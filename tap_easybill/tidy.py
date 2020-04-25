from singer import Transformer
from singer import utils, metadata

def tidy_response(stream, raw_row):

    with Transformer() as transformer:
        tidy_row = transformer.transform(raw_row, stream.schema.to_dict(), metadata.to_map(stream.metadata))

    return tidy_row
