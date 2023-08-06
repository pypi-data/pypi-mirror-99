''' RestAdapter is a helper class for managing http calls to Instance Manager '''

import logging
from requests import request, HTTPError, codes
from sap.instance_manager.constants import ENDPOINT


class RestAdapter:
    ''' RestAdapter '''

    def __init__(self, options):
        self._options = options

    def get_all_instances(self):
        ''' Gets all instances from the managed service '''
        req_options = self._build_options(ENDPOINT['GET_ALL'])
        try:
            res = request(req_options['method'], req_options['url'], auth=req_options['auth'])
        except HTTPError as exc:
            message = 'Error ocurred while getting all instances'
            _handle_network_error(exc, message)

        if res.status_code != codes['ok']:
            message = 'Unexpected response while getting all instances'
            _report_unexpected_status_error(res.status_code, message)

        return _safe_parse(res)

    def init_create_instance(self, tenant, optional_parameters):
        ''' Calls managed service to create instance '''
        req_options = self._build_options(ENDPOINT['CREATE'], tenant)
        try:
            res = request(req_options['method'], req_options['url'],
                          auth=req_options['auth'], json=optional_parameters)
        except HTTPError as exc:
            message = 'Error ocurred while creating instance for tenant "{0}"'.format(tenant)
            _handle_network_error(exc, message)

        # codes.created is actually stating that the creation has started
        # but might not be completed
        if res.status_code != codes['created']:
            message = 'Unexpected response while creating instance for tenant "{0}"'.format(tenant)
            _report_unexpected_status_error(res.status_code, message)

    def get_instance(self, tenant):
        ''' Gets specific instance from the managed service '''
        req_options = self._build_options(ENDPOINT['GET'], tenant)
        try:
            res = request(req_options['method'], req_options['url'], auth=req_options['auth'])
        except HTTPError as exc:
            message = 'Error ocurred while getting instance for tenant "{0}"'.format(tenant)
            _handle_network_error(exc, message)

        if res.status_code == codes['not_found']:
            logging.debug('Instance for tenant "%s" not found', tenant)
            return None

        if res.status_code != codes['ok']:
            message = 'Unexpected response while getting instance for tenant "{0}"'.format(tenant)
            _report_unexpected_status_error(res.status_code, message)

        return _safe_parse(res)

    def init_delete_instance(self, tenant):
        ''' Deletes specific instance from the managed service '''
        req_options = self._build_options(ENDPOINT['DELETE'], tenant)
        try:
            res = request(req_options['method'], req_options['url'], auth=req_options['auth'])
        except HTTPError as exc:
            message = 'Error ocurred during deletion of instance for tenant "{0}"'.format(tenant)
            _handle_network_error(exc, message)

        # codes.no_content is actually stating that the deletion has started
        # but might not be completed
        if res.status_code != codes['no_content']:
            message = 'Unexpected response while deleting instance for tenant "{0}"'.format(tenant)
            _report_unexpected_status_error(res.status_code, message)

    def _build_options(self, endpoint, tenant=None):
        url = self._options[endpoint['name']]
        if tenant:
            url = url.replace('{tenant_id}', tenant)
        return {
            'method': endpoint['method'],
            'url': url,
            'auth': (self._options['user'], self._options['password'])
        }


def _handle_network_error(exception, message):
    logging.debug(message)
    if not exception.args:
        exception.args = ('',)
    exception.args += (message,)
    raise exception


def _report_unexpected_status_error(status, message):
    error_message = message + ', status code: ' + str(status)
    logging.debug(error_message)
    raise HTTPError(error_message)


def _safe_parse(response):
    try:
        return response.json()
    except ValueError as exc:
        message = 'Error ocurred while parsing the response'
        if not exc.args:
            exc.args = ('',)
        exc.args += (message,)
        raise exc
