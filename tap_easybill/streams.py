from singer import metadata

BASE_METADATA = {
    'document-payments': {
        'selected': True,
        'endpoint_path': '/document-payments',
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_key_coalesce': False,
        'replication_key': 'id',
        'replication_sorted': True
    },
    'documents': {
        'selected': True,
        'endpoint_path': '/documents',
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_key_coalesce': True,
        'replication_key': ['edited_at', 'created_at'],
        'replication_sorted': False
    },
    'post-boxes': {
        'selected': True,
        'endpoint_path': '/post-boxes',
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_key_coalesce': True,
        'replication_key': ['processed_at', 'create_at'],
        'replication_sorted': False
    }
}

def gen_metadata(stream_id, schema, base_metadata):
    full_metadata = metadata.get_standard_metadata(schema.to_dict())
    for k, v in base_metadata[stream_id].items():
        metadata.write(metadata.to_map(full_metadata), (), k, v)

    return full_metadata
