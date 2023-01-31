import requests
from configs import WINDOW_START, WINDOW_END, COVID_CASES_ADDRESS, COVID_API_URL, SELECTED_PROVINCE


def fetch_covid_cases():
    result = requests.get(COVID_API_URL,
                          params={'fmt': 'csv', 'legacy': 'false', 'hr_names': 'hruid', 'pt_names': 'short',
                                  'fill': 'true', 'after': WINDOW_START, 'before': WINDOW_END,
                                  'loc': SELECTED_PROVINCE, 'geo': 'pt', 'stat': 'cases'})
    if result.status_code != 200:
        raise RuntimeError('API Call Status Code : {}'.format(result.status_code))

    f = open(COVID_CASES_ADDRESS, 'w')
    f.write(result.content.decode('UTF-8'))
