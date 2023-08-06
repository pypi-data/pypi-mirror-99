''' Instance Manager client class. '''

import logging
from sap.instance_manager.lru_cache import LRUCache
from sap.instance_manager.adapter import RestAdapter
from sap.instance_manager.polling_util import Polling
from sap.instance_manager.constants import INSTANCE
from sap.instance_manager.user_input import process_main_options, process_tenant


class InstanceManager:
    ''' InstanceManager '''

    def __init__(self, options):
        self._adapter = RestAdapter(options)
        self._polling = Polling(self._adapter,
                                options['polling_interval_millis'],
                                options['polling_timeout_seconds'])
        self._cache = LRUCache(
            options['cache_max_items'],
            float(options['cache_item_expire_seconds']))

    def create(self, tenant, optional_parameters=None):
        ''' create instance '''
        tenant = process_tenant(tenant)
        if optional_parameters is not None and not isinstance(optional_parameters, dict):
            raise RuntimeError(
                'instance_manager.create: optional_parameters must be a dict')
        self._adapter.init_create_instance(tenant, optional_parameters)
        instance = self._polling.until_created(tenant)
        if not instance:
            raise RuntimeError('Instance for tenant {0} not found'.format(tenant))
        self._cache.add(tenant, instance)
        return instance

    def get(self, tenant):
        ''' get instance '''
        tenant = process_tenant(tenant)
        cache_entry = self._cache.get(tenant)
        if cache_entry:
            logging.debug(
                'Getting instance for tenant "%s" from cache', tenant)
            return cache_entry
        instance = self._polling.until_created(tenant)
        if instance:
            self._cache.add(tenant, instance)
        return instance

    def get_all(self):
        ''' get all instances '''
        instances = self._adapter.get_all_instances()
        self._cache.clear()

        for instance in instances:
            if instance['status'] == INSTANCE['CREATED']:
                self._cache.add(instance['tenant_id'], instance)

        return instances

    def delete(self, tenant):
        ''' delete instance '''
        tenant = process_tenant(tenant)
        self._cache.remove(tenant)
        self._adapter.init_delete_instance(tenant)
        self._polling.until_deleted(tenant)


def create(options):
    ''' Creates InstanceManager Client '''
    opts = process_main_options(options)

    instance_manager = InstanceManager(opts)
    instance_manager.get_all()
    return instance_manager
