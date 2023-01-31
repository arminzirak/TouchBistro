import pandas as pd

WINDOW_START = "2020-03-20"
WINDOW_END = "2021-01-01"

restaurant_revenues = pd.read_excel('./data/takehome_exercise_v2.xlsx', sheet_name='Sample Restaurant Revenue')
restaurant_revenues_ontario = restaurant_revenues[restaurant_revenues['Province'] == 'ON']
# restaurant_revenues_ontario['Date'] = restaurant_revenues_ontario['Date'] + pd.offsets.DateOffset(years=2)
restaurant_revenues_ontario_timeFiltered = restaurant_revenues_ontario[
    (WINDOW_END >= restaurant_revenues_ontario['Date']) & (restaurant_revenues_ontario['Date'] >= WINDOW_START)]

cases = pd.read_csv('data/timeseries.csv')
cases['week'] = pd.to_datetime(cases['date']).dt.week
cases['day'] = pd.to_datetime(cases['date']).dt.dayofweek
cases['corrected_week'] = cases['week'] + (cases['day'] >= 4)
cases_aggregated = cases.groupby('corrected_week').agg({'value_daily': ['max', 'min', 'mean', 'var'],
                                                        'date': ['min', 'max']}).reset_index()

restaurant_revenues_ontario_timeFiltered['week'] = restaurant_revenues_ontario_timeFiltered['Date'].dt.week
restaurant_revenues_ontario_timeFiltered['day'] = restaurant_revenues_ontario_timeFiltered['Date'].dt.dayofweek
restaurant_revenues_ontario_timeFiltered['corrected_week'] = \
    restaurant_revenues_ontario_timeFiltered['week'] + (restaurant_revenues_ontario_timeFiltered['day'] >= 4)

restaurant_revenues_ontario_timeFiltered_aggregated = \
    restaurant_revenues_ontario_timeFiltered \
        .groupby(['Restaurant ID', 'corrected_week']).agg({'Revenue': ['max', 'min', 'sum', 'var']}).reset_index()

restaurant_revenues_ontario_timeFiltered_aggregated.loc[:, ('Revenue', 'average')] \
    = restaurant_revenues_ontario_timeFiltered_aggregated.loc[:, ('Revenue', 'sum')] / 7

print(len(cases_aggregated), len(restaurant_revenues_ontario_timeFiltered_aggregated))
combined_data = pd.merge(restaurant_revenues_ontario_timeFiltered_aggregated,
                         cases_aggregated, on='corrected_week')

combined_data.to_csv('./output/results.csv')