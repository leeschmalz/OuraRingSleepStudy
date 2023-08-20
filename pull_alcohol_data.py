from exist_api_client import getExistAttribute
import pandas as pd

alcohol_data = getExistAttribute('alcoholic_drinks', count=9999)

rows = []
for entry in alcohol_data:
    rows.append({'date': entry['date'], 'name': 'alcohol', 'value': entry['value']})

df = pd.DataFrame(rows)

# read old manually recorded data
df_old = pd.read_csv('./data/old_manual_alcohol_data.csv')

df['date'] = pd.to_datetime(df['date'])
df_old['date'] = pd.to_datetime(df_old['date'], format='%m/%d/%y')  # based on the old format '4/17/22'

# Combine the dataframes
df_combined = pd.concat([df, df_old], ignore_index=True)
df_combined = df_combined.sort_values(by='date', ascending=True).reset_index(drop=True)

df_combined.to_csv('./data/alcohol_data.csv', index=False)