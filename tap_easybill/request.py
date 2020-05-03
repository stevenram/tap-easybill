import requests
import json
import os
import singer
from singer import utils, metadata
import math

LOGGER = singer.get_logger()

def tap_api(stream, state):

    endpoint_path = metadata.get(metadata.to_map(stream.metadata), (), 'endpoint_path')
    replication_sorted = metadata.get(metadata.to_map(stream.metadata), (), 'replication_sorted')
    page_scan_perc = metadata.get(metadata.to_map(stream.metadata), (), 'page_scan_perc')
    page_state = singer.get_bookmark(state, stream.tap_stream_id, 'page')

    endpoint = 'https://api.easybill.de/rest/v1'+endpoint_path
    headers = {'Authorization': 'Bearer ' + os.environ['EASYBILL_KEY'] }

    if replication_sorted:
        page = page_state or 1
    else:
        page = max(math.floor(page_state*(1-page_scan_perc)), 1) or 1

    while True:
        params = {'page': page}
        # params = {'page': page, 'limit': 20}
        LOGGER.info("Requesting and scanning page: " + str(page))
        r = requests.get(endpoint, headers=headers, params=params)
        r = r.json()
        data = r['items']

        number_datapoints = len(data)
        for each in range(0, number_datapoints):
            yield data[each], page

        if r['page'] == r['pages']:
        # if r['page'] == 3:
            break
        else:
            page += 1
