from singer import Transformer
from singer import utils, metadata

def tidy_response(stream, raw_row, needs_coalescing, replication_key):

    if needs_coalescing:
        bookmark_value = raw_row[replication_key[0]] or raw_row[replication_key[1]]
    else:
        bookmark_value = raw_row[replication_key]

    with Transformer() as transformer:
        tidy_row = transformer.transform(raw_row, stream.schema.to_dict(), metadata.to_map(stream.metadata))

    return tidy_row, bookmark_value
