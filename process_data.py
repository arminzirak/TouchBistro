import pandas as pd

restaurant_revenues = pd.read_excel('./data/takehome_exercise_v2.xlsx', sheet_name='Sample Restaurant Revenue')
restaurant_revenues_ontario = restaurant_revenues[restaurant_revenues['Province'] == 'ON']
restaurant_revenues_ontario['Date'] = restaurant_revenues_ontario['Date'] + pd.offsets.DateOffset(years=2)
restaurant_revenues_ontario_timeFiltered = restaurant_revenues_ontario[
    ("2023-01-01" >= restaurant_revenues_ontario['Date']) & (restaurant_revenues_ontario['Date'] >= "2022-03-20")]

cases = pd.read_csv('data/timeseries.csv')
cases['week'] = pd.to_datetime(cases['date']).dt.week
cases['day'] = pd.to_datetime(cases['date']).dt.dayofweek
cases['corrected_week'] = cases['week'] + (cases['day'] == 6)
cases_aggregated = cases.groupby('corrected_week').agg({'value_daily': ['max', 'min', 'mean', 'var'],
                                                        'date': ['min', 'max']}).reset_index()

restaurant_revenues_ontario_timeFiltered['week'] = restaurant_revenues_ontario_timeFiltered['Date'].dt.week
restaurant_revenues_ontario_timeFiltered['day'] = restaurant_revenues_ontario_timeFiltered['Date'].dt.dayofweek
restaurant_revenues_ontario_timeFiltered['corrected_week'] = \
    restaurant_revenues_ontario_timeFiltered['week'] + (restaurant_revenues_ontario_timeFiltered['day'] == 6)

restaurant_revenues_ontario_timeFiltered_aggregated = \
    restaurant_revenues_ontario_timeFiltered \
        .groupby(['Restaurant ID', 'corrected_week']).agg({'Revenue': ['max', 'min', 'mean', 'var'],
                                                           'Date': ['min', 'max']}).reset_index()

combined_data = pd.merge(restaurant_revenues_ontario_timeFiltered_aggregated,
                         cases_aggregated, on='corrected_week')
