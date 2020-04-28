from singer import Transformer
from singer import utils, metadata

def tidy_response(stream, raw_row):

    # Make edited_at a safe replication key by coalsceing with created_at
    if stream.tap_stream_id == 'documents':
        raw_row['edited_at_rk'] = raw_row['edited_at'] or raw_row['create_at']

    with Transformer() as transformer:
        tidy_row = transformer.transform(raw_row, stream.schema.to_dict(), metadata.to_map(stream.metadata))

    return tidy_row
