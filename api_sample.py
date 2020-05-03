import requests
import os
import json


endpoint = 'https://api.easybill.de/rest/v1/document-payments?limit=1'
headers = {'Authorization': 'Bearer ' + os.environ['EASYBILL_KEY'] }

r = requests.get(endpoint, headers=headers)
r = r.json()

dump = False
with open('api_sample.json', 'w') as f:
    if dump:
        json.dump(r, f)


# data = r['items']
# for each in range(0, len(data)):
#     print(each, ' ', data[each]['create_at'], ' ', data[each]['processed_at'] or data[each]['create_at'])

print(r)
