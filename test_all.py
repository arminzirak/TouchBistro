from fetch import fetch_covid_cases
from process_data import process_data
import os
from configs import RESTAURANTS_REVENUE_ADDRESS, RESULTS_ADDRESS, COVID_CASES_ADDRESS, WINDOW_START, WINDOW_END, SELECTED_PROVINCE
import pytest
import shutil
from unittest.mock import patch
import requests

import pandas as pd


def get_backup_name(name):
    return f'{name}.bc'


@pytest.fixture(autouse=True)
def run_around_tests():
    COVID_CASES_BACKUP = get_backup_name(COVID_CASES_ADDRESS)
    RESTAURANTS_REVENUE_BACKUP = get_backup_name(RESTAURANTS_REVENUE_ADDRESS)
    RESULTS_BACKUP = get_backup_name(RESULTS_ADDRESS)

    if os.path.exists(COVID_CASES_ADDRESS):
        shutil.copyfile(COVID_CASES_ADDRESS, COVID_CASES_BACKUP)

    if os.path.exists(RESTAURANTS_REVENUE_ADDRESS):
        shutil.copyfile(RESTAURANTS_REVENUE_ADDRESS, RESTAURANTS_REVENUE_BACKUP)

    if os.path.exists(RESULTS_ADDRESS):
        shutil.copyfile(RESULTS_ADDRESS, RESULTS_BACKUP)

    yield

    if os.path.exists(COVID_CASES_BACKUP):
        os.replace(COVID_CASES_BACKUP, COVID_CASES_ADDRESS)

    if os.path.exists(RESTAURANTS_REVENUE_BACKUP):
        os.replace(RESTAURANTS_REVENUE_BACKUP, RESTAURANTS_REVENUE_ADDRESS)

    if os.path.exists(RESULTS_BACKUP):
        os.replace(RESULTS_BACKUP, RESULTS_ADDRESS)


def test_fetch_covid_cases():
    if os.path.exists(COVID_CASES_ADDRESS):
        os.remove(COVID_CASES_ADDRESS)

    fetch_covid_cases()

    assert os.path.exists(COVID_CASES_ADDRESS), 'No file is created'

    fetched_data = pd.read_csv(COVID_CASES_ADDRESS)

    assert len(fetched_data), 'No data is fetched'
    assert (fetched_data['region'] == SELECTED_PROVINCE).all()
    assert (fetched_data['date'] >= WINDOW_START).all()
    assert (fetched_data['date'] <= WINDOW_END).all()


@patch('requests.get')
def test_request_post_exception(self, requests_mock):
    if os.path.exists(COVID_CASES_ADDRESS):
        os.remove(COVID_CASES_ADDRESS)

    requests_mock.side_effect = requests.exceptions.ConnectionError()

    with pytest.raises(RuntimeError):
        fetch_covid_cases()

    assert not os.path.exists(COVID_CASES_ADDRESS)


def test_process_data():
    if os.path.exists(RESULTS_ADDRESS):
        os.remove(RESULTS_ADDRESS)

    process_data()

    assert os.path.exists(RESULTS_ADDRESS)

    results = pd.read_csv(RESULTS_ADDRESS, header=[0, 1], skipinitialspace=True)

    assert len(results)

    assert ('Revenue', 'max') in results.columns
    assert ('Revenue', 'min') in results.columns
    assert ('Revenue', 'average') in results.columns
    assert ('Revenue', 'var') in results.columns

    assert ('covid_cases_daily', 'max') in results.columns
    assert ('covid_cases_daily', 'min') in results.columns
    assert ('covid_cases_daily', 'mean') in results.columns
    assert ('covid_cases_daily', 'var') in results.columns

    assert ('date', 'max') in results.columns
    assert ('date', 'min') in results.columns
    assert (results['date'].max() <= WINDOW_END).all()
    assert (results['date'].min() >= WINDOW_START).all()


def test_process_data_missing_covid_cases():
    if os.path.exists(COVID_CASES_ADDRESS):
        os.remove(COVID_CASES_ADDRESS)
    if os.path.exists(RESULTS_ADDRESS):
        os.remove(RESULTS_ADDRESS)

    with pytest.raises(FileNotFoundError):
        process_data()

    assert not os.path.exists(RESULTS_ADDRESS)


#
def test_process_data_missing_restaurant_revenues():
    if os.path.exists(RESTAURANTS_REVENUE_ADDRESS):
        os.remove(RESTAURANTS_REVENUE_ADDRESS)
    if os.path.exists(RESULTS_ADDRESS):
        os.remove(RESULTS_ADDRESS)

    with pytest.raises(FileNotFoundError):
        process_data()

    assert not os.path.exists(RESULTS_ADDRESS)
