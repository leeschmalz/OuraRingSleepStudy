import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
import csv
load_dotenv()

oura_token = os.environ.get('OURA_TOKEN')

def getSleepData(day='2023-08-09'):
    '''
    Get sleep data for a single day
    '''
    url = 'https://api.ouraring.com/v2/usercollection/sleep' 

    params={ 
        'start_date': day, 
        'end_date': (datetime.strptime(day, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') # next day
    }

    headers = { 
    'Authorization': f'Bearer {oura_token}' 
    }

    response = requests.request('GET', url, headers=headers, params=params)

    return response.json()['data'][0]

def parseBedTimefromSleep(sleep_data):
    bedtime_start = datetime.fromisoformat(sleep_data['bedtime_start'])
    bedtime_end = datetime.fromisoformat(sleep_data['bedtime_end'])

    return bedtime_start, bedtime_end

def parseHRfromSleep(sleep_data):
    hr = sleep_data['heart_rate']

    timestamp = datetime.fromisoformat(hr['timestamp'])
    interval = timedelta(seconds=hr['interval'])

    result = []
    for item in hr['items']:
        if item is not None:
            result.append((timestamp, item))
        timestamp += interval

    return result

def writeTimeSeriesData(data, file_name, value_column_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['time', value_column_name])

        for row in data:
            # Convert the datetime object to a string, if needed
            time_str = row[0].strftime('%Y-%m-%d %H:%M')
            value = row[1]

            writer.writerow([time_str, value])

    print(f"{file_name} written successfully.")

if __name__ == '__main__':
    sleep = getSleepData()
    pretty_sleep = json.dumps(sleep, indent=4)  # Indent with 4 spaces
    print(pretty_sleep)
    hr = parseHRfromSleep(sleep)
    writeTimeSeriesData(hr, 
                        file_name='./data/heartrate_sleep_example.csv', 
                        value_column_name='heartrate')