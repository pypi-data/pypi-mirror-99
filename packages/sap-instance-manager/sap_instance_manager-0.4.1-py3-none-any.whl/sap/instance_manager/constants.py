''' Constants used by the Instance Manager client. '''

ENDPOINT = {
    'CREATE': {
        'method': 'POST',
        'name': 'post_managed_instance_url'
    },
    'GET': {
        'method': 'GET',
        'name': 'get_managed_instance_url'
    },
    'GET_ALL': {
        'method': 'GET',
        'name': 'get_all_managed_instances_url'
    },
    'DELETE': {
        'method': 'DELETE',
        'name': 'delete_managed_instance_url'
    }
}

INSTANCE = {
    'CREATING': 'CREATION_IN_PROGRESS',
    'CREATED': 'CREATION_SUCCEEDED',
    'FAILED_CREATION': 'CREATION_FAILED',
    'DELETING': 'DELETION_IN_PROGRESS',
    'FAILED_DELETION': 'DELETION_FAILED'
}

DEFAULT_OPTIONS = {
    'cache_max_items': 500,
    'cache_item_expire_seconds': 10 * 60,
    'polling_interval_millis': 300,
    'polling_timeout_seconds': 120
}

OPTIONS_SCHEMA = {
    'type': 'object',
    'properties': {
        'user': {'type': 'string', 'minLength': 1},
        'password': {'type': 'string', 'minLength': 1},
        'post_managed_instance_url': {'type': 'string', 'minLength': 1},
        'get_managed_instance_url': {'type': 'string', 'minLength': 1},
        'get_all_managed_instances_url': {'type': 'string', 'minLength': 1},
        'delete_managed_instance_url': {'type': 'string', 'minLength': 1},
        'polling_interval_millis': {'type': 'integer', 'minimum': 0},
        'polling_timeout_seconds': {'type': 'integer', 'minimum': 1},
        'cache_max_items': {'type': 'integer', 'minimum': 1},
        'cache_item_expire_seconds': {'type': 'integer', 'minimum': 1}
    },
    'required': ['user', 'password', 'post_managed_instance_url', 'get_managed_instance_url',
                 'get_all_managed_instances_url', 'delete_managed_instance_url']
}
