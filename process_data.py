import pandas as pd
from configs import COVID_CASES_ADDRESS, WINDOW_START, WINDOW_END, \
    RESTAURANTS_REVENUE_ADDRESS, RESTAURANTS_REVENUE_SHEET, RESULTS_ADDRESS, \
    FIRST_DAY_OF_WEEK, SELECTED_PROVINCE
import os


def process_data():
    if not os.path.exists(COVID_CASES_ADDRESS) or not os.path.exists(RESTAURANTS_REVENUE_ADDRESS):
        raise FileNotFoundError('Input data is not provided')

    revenues = pd.read_excel(RESTAURANTS_REVENUE_ADDRESS, sheet_name=RESTAURANTS_REVENUE_SHEET)
    revenues = revenues[revenues['Province'] == SELECTED_PROVINCE]
    revenues = revenues[
        (WINDOW_END >= revenues['Date']) & (revenues['Date'] >= WINDOW_START)]

    revenues['week'] = revenues['Date'].dt.isocalendar().week
    revenues['day'] = revenues['Date'].dt.dayofweek
    revenues['corrected_week'] = revenues['week'] + (revenues['day'] >= FIRST_DAY_OF_WEEK)

    revenues_aggregated = revenues \
        .groupby(['Restaurant ID', 'corrected_week']) \
        .agg({'Revenue': ['max', 'min', 'sum', 'var']}) \
        .reset_index()
    revenues_aggregated.loc[:, ('Revenue', 'average')] = revenues_aggregated.loc[:, ('Revenue', 'sum')] / 7

    covid_cases = pd.read_csv(COVID_CASES_ADDRESS)
    covid_cases.loc[:, 'week'] = pd.to_datetime(covid_cases['date']).dt.isocalendar().week
    covid_cases.loc[:, 'day'] = pd.to_datetime(covid_cases['date']).dt.dayofweek
    covid_cases.loc[:, 'corrected_week'] = covid_cases['week'] + (covid_cases['day'] >= FIRST_DAY_OF_WEEK)
    covid_cases.rename(columns={'value_daily': 'covid_cases_daily'}, inplace=True)
    covid_cases_aggregated = covid_cases \
        .groupby('corrected_week') \
        .agg({'covid_cases_daily': ['max', 'min', 'mean', 'var'], 'date': ['min', 'max']}) \
        .reset_index()

    combined_data = pd.merge(revenues_aggregated, covid_cases_aggregated, on='corrected_week')
    combined_data.to_csv(RESULTS_ADDRESS)
    return True