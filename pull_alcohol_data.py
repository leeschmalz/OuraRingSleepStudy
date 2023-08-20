from exist_api_client import getExistAttribute

alcohol_data = getExistAttribute('alcoholic_drinks', count=9999)

rows = []
for entry in alcohol_data:
    rows.append({'date': entry['date'], 'name': 'alcohol', 'value': entry['value']})

# write to csv
import pandas as pd
df = pd.DataFrame(rows)
df.to_csv('./data/alcohol_data.csv', index=False)