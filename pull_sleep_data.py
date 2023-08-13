from oura_api_client import *
from tqdm import tqdm

# iterate over ['2022-01-01', ..., '2023-08-12']
dates = [datetime.strftime(datetime.strptime('2022-01-01', '%Y-%m-%d') + timedelta(days=i), '%Y-%m-%d') for i in range(0, 588)]

for date in tqdm(dates):
    # TODO: Handle days where Ring was dead or not worn and no data was collected
    # TODO: Handle days with naps
    sleep_data = getSleepData(date)
    hr_data1 = parseHRfromSleep(sleep_data)
    if date != dates[0]:
        # bind
        hr_data = hr_data + hr_data1
    else:
        hr_data = hr_data1
        
    


writeTimeSeriesData(hr_data, f'./data/sleep_heartrate_data.csv', 'hr')