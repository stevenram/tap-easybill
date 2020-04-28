import requests
import os
import json


endpoint = 'https://api.easybill.de/rest/v1/documents?limit=100&page=319'
headers = {'Authorization': 'Bearer ' + os.environ['EASYBILL_KEY'] }

r = requests.get(endpoint, headers=headers)
r = r.json()

print(r)
