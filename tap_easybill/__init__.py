#!/usr/bin/env python3
import os
import json
import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from tap_easybill.request import tap_api
from tap_easybill.tidy import tidy_response
from tap_easybill.streams import gen_metadata, BASE_METADATA


REQUIRED_CONFIG_KEYS = []
LOGGER = singer.get_logger()

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():

        stream_metadata = gen_metadata(stream_id, schema, BASE_METADATA)

        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=metadata.get(metadata.to_map(stream_metadata), (), 'key_properties'),
                metadata=stream_metadata
            )
        )

    return Catalog(streams)


def sync(config, state, catalog):

    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        LOGGER.info("Syncing stream: " + stream.tap_stream_id)

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties
        )

        needs_coalescing = metadata.get(metadata.to_map(stream.metadata), (), 'replication_key_coalesce')
        replication_key = metadata.get(metadata.to_map(stream.metadata), (), 'replication_key')
        replication_sorted = metadata.get(metadata.to_map(stream.metadata), (), 'replication_sorted')

        bookmark_state = singer.get_bookmark(state, stream.tap_stream_id, 'value')
        new_bookmark_state = bookmark_state
        page_state = singer.get_bookmark(state, stream.tap_stream_id, 'page')
        new_page_state = page_state

        # for row, page in tap_api(stream.tap_stream_id, page_state):
        for row, page in tap_api(stream, state):

            row, bookmark_value = tidy_response(stream, row, needs_coalescing, replication_key)

            if bookmark_value > bookmark_state:
                singer.write_record(stream.tap_stream_id, row)

                if replication_sorted and not needs_coalescing:
                    singer.write_bookmark(state, stream.tap_stream_id, 'value', row[replication_key])
                    singer.write_bookmark(state, stream.tap_stream_id, 'page', page)
                    singer.write_state(state)
                else:
                    new_bookmark_state = max(bookmark_state, bookmark_value)
                    new_page_state = page

        if new_bookmark_state > bookmark_state:
            singer.write_bookmark(state, stream.tap_stream_id, 'value', new_bookmark_state)
            singer.write_bookmark(state, stream.tap_stream_id, 'page', new_page_state)
            singer.write_state(state)

    return state


def save_state_json(state):
    with open('state.json', 'w') as file:
        json.dump(state, file)


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # Load state from json or initialize empty state
    state = args.state or {}

    # Load config from json
    config = args.config

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        catalog = args.catalog or discover()
        new_state = sync(config, state, catalog)
        save_state_json(new_state)

if __name__ == "__main__":
    main()
