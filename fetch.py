import requests
from configs import WINDOW_START, WINDOW_END, COVID_CASES_ADDRESS, COVID_API_URL


def fetch_covid_cases():
    print(COVID_API_URL)
    result = requests.get(COVID_API_URL,
                          params={'fmt': 'csv', 'legacy': 'false', 'hr_names': 'hruid', 'pt_names': 'short',
                                  'fill': 'true', 'after': WINDOW_START, 'before': WINDOW_END,
                                  'loc': 'ON', 'geo': 'pt', 'stat': 'cases'})
    f = open(COVID_CASES_ADDRESS, 'w')
    f.write(result.content.decode('UTF-8'))
    return True
