''' Polling utilities for instance creation and deletion. '''

import time
from requests import HTTPError
from sap.instance_manager.constants import INSTANCE

class TimeoutException(Exception):
    ''' Exception raised if polling function times out '''

class Polling:
    ''' Polling '''

    def __init__(self, rest_adapter, interval_milliseconds, timeout_seconds):
        self._rest_adapter = rest_adapter
        self._interval_seconds = interval_milliseconds / 1000.0
        self._timeout_seconds = timeout_seconds

    def until_created(self, tenant):
        ''' poll until instance is created '''
        return self._poll_status(tenant, _is_created)

    def until_deleted(self, tenant):
        ''' poll until instance is deleted '''
        self._poll_status(tenant, _is_deleted)

    def _poll_status(self, tenant, check_success):
        ''' poll until required state is reached '''
        start_time = time.time()
        while time.time() - start_time < self._timeout_seconds:
            try:
                instance = self._rest_adapter.get_instance(tenant)
                if check_success(instance):
                    return instance
            except HTTPError:
                pass
            time.sleep(self._interval_seconds)
        raise TimeoutException('Timeout waiting for instance for tenant {0}'.format(tenant))

def _is_created(instance):
    if not instance or instance['status'] == INSTANCE['CREATED']:
        return True

    _check_invalid_status(instance, 'CREATING')
    return False


def _is_deleted(instance):
    if not instance:
        return True

    _check_invalid_status(instance, 'DELETING')
    return False


def _check_invalid_status(instance, valid_status):
    if not instance['status'] == INSTANCE[valid_status]:
        message = 'Status of instance for tenant "{0}" is {1}'.format(
            instance['tenant_id'], instance['status']
        )
        if 'failed_message' in instance:
            message += '. Reason: {0}.'.format(instance['failed_message'])

        raise RuntimeError(message)
