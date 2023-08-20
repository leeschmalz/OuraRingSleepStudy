import requests
import os
from dotenv import load_dotenv
load_dotenv()

def getExistAttribute(attribute, count):
    exist_token = os.environ.get("EXIST_TOKEN")
    results = []
    
    page_size = 100  # Assuming the maximum page size is 100

    page = 1
    last_page = 999
    while page <= last_page:
        
        searchParams = {
            "attribute": attribute,
            "limit": page_size,
            "page": page
        }
        
        url = "https://exist.io/api/2/attributes/values/?"
        response = requests.get(url, params=searchParams, headers={
            "Authorization": f"Token {exist_token}"
        })

        if page==1:
            last_page = (response.json()['count'] + page_size - 1) // page_size

        if response.status_code == 200:
            data = response.json()
            results.extend(data['results'])
        else:
            print(f"Failed with status code: {response.status_code}")
            return None

        page += 1

    return results[:count]

if __name__ == "__main__":
    # attributes: 'workouts_distance', 'weight_lifting', 'pages_read', 'alcoholic_drinks'
    data1 = getExistAttribute('cycle_distance', count=2)
    data2 = getExistAttribute('workouts_distance', count=2)
    print(data1)
    print(data2)