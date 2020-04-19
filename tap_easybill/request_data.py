import requests
import json
import os


def tap_data(stream_id):

    endpoint = 'https://api.easybill.de/rest/v1/'+stream_id
    headers = {'Authorization': 'Bearer ' + os.environ['EASYBILL_KEY'] }

    next_page = 1
    while True:
        # params = {'page': next_page}
        params = {'page': next_page, 'limit': 2}
        r = requests.get(endpoint, headers=headers, params=params)
        r = r.json()

        data = r['items']

        number_datapoints = len(data)
        for each in range(0, number_datapoints):
        # To do:
        # Need to handle nested objects in the documents schema
        # Potentially flatten, or serialize into string if easier, or exclude
        # In any case, need to add a transform step
            if not stream_id == 'documents':
                yield data[each]
            else:
                yield {
                    'id': data[each]['id'],
                    'is_draft': data[each]['is_draft']
                }

        # if r['page'] == r['pages']:
        if r['page'] == 2:
            break
        else:
            next_page += 1
