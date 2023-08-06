''' User input validation utilities '''

from jsonschema import validate
from sap.instance_manager.constants import OPTIONS_SCHEMA, DEFAULT_OPTIONS

def process_main_options(options):
    ''' validates and sets default options given to instance_manager.create '''
    validate(options, OPTIONS_SCHEMA)
    return dict(DEFAULT_OPTIONS, **options)

def process_tenant(tenant):
    ''' validates tenant '''
    validate(tenant, {'type': 'string'})
    tenant = tenant.strip()
    validate(tenant, {'minLength': 1})
    return tenant
