import requests
import json
import os


def tap_api(stream):

    endpoint = 'https://api.easybill.de/rest/v1/'+stream
    headers = {'Authorization': 'Bearer ' + os.environ['EASYBILL_KEY'] }

    next_page = 1
    while True:
        # params = {'page': next_page}
        params = {'page': next_page, 'limit': 1}
        r = requests.get(endpoint, headers=headers, params=params)
        r = r.json()

        data = r['items']

        number_datapoints = len(data)
        for each in range(0, number_datapoints):
            yield data[each]

        # if r['page'] == r['pages']:
        if r['page'] == 1:
            break
        else:
            next_page += 1
