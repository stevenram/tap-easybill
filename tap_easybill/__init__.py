#!/usr/bin/env python3
import os
import json
import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from tap_easybill.request import tap_api
from tap_easybill.tidy import tidy_response


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

        # Generate minimum required metadata and select every stream
        min_metadata = metadata.get_standard_metadata(schema.to_dict())
        metadata.write(metadata.to_map(min_metadata), (), "selected", True)

        stream_metadata = min_metadata
        key_properties = ['id'] # So far all of the streams have this key property
        if stream_id in ('documents'):
            replication_key = 'edited_at_rk'
        else:
            replication_key = 'id'

        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=replication_key,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method='INCREMENTAL'
            )
        )

    return Catalog(streams)


def sync(config, state, catalog):

    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        bookmark_column = stream.replication_key

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        max_bookmark = singer.get_bookmark(state, stream.tap_stream_id, bookmark_column)
        page_state = singer.get_bookmark(state, stream.tap_stream_id, 'page')


        for row, page in tap_api(stream.tap_stream_id, page_state):

            # TO DO: Place type conversions or transformations here
            row = tidy_response(stream, row)

            # Write one or more rows to the stream:
            if row[bookmark_column] > max_bookmark:
                singer.write_records(stream.tap_stream_id, [row])
                new_max_bookmark = max(max_bookmark, row[bookmark_column])

                singer.write_bookmark(state, stream.tap_stream_id, bookmark_column, new_max_bookmark)
                singer.write_bookmark(state, stream.tap_stream_id, 'page', page)
                singer.write_state(state)

            # Write state messages

        #     if bookmark_column:
        #         if is_sorted:
        #             # update bookmark to latest value
        #             singer.write_state({stream.tap_stream_id: row[bookmark_column]})
        #         else:
        #             # if data unsorted, save max value until end of writes
        #             max_bookmark = max(max_bookmark, row[bookmark_column])
        # if bookmark_column and not is_sorted:
        #     singer.write_state({stream.tap_stream_id: max_bookmark})

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
    print('========== STATE LOADED AS ', state)

    # Load config from json
    config = args.config

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        catalog = args.catalog or discover()
        state = sync(config, state, catalog)
        save_state_json(state)

if __name__ == "__main__":
    main()
