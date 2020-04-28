import requests
import json
import os


def tap_api(stream, page_state):

    endpoint = 'https://api.easybill.de/rest/v1/'+stream
    headers = {'Authorization': 'Bearer ' + os.environ['EASYBILL_KEY'] }

    page = page_state or 1
    while True:
        # params = {'page': page}
        params = {'page': page, 'limit': 20}
        print('======== PAGE ', page)
        r = requests.get(endpoint, headers=headers, params=params)
        r = r.json()

        data = r['items']

        number_datapoints = len(data)
        for each in range(0, number_datapoints):
            yield data[each], page

        # if r['page'] == r['pages']:
        if r['page'] == 3:
            break
        else:
            page += 1
