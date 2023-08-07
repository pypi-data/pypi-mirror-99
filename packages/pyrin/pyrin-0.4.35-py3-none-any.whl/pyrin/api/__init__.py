# -*- coding: utf-8 -*-
"""
api package.
"""

import pyrin.application.services as application_services

from pyrin.packaging.base import Package


class APIPackage(Package):
    """
    api package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration',
               'pyrin.logging']

    COMPONENT_NAME = 'api.component'
    CONFIG_STORE_NAMES = ['api']

    def _load_configs(self, config_services):
        """
        loads all required configs of this package.
        this method is intended for overriding by
        subclasses to do custom configurations.

        :param Module config_services: configuration services dependency.
                                       to be able to overcome circular dependency problem,
                                       we should inject configuration services dependency
                                       into this method. because all other packages are
                                       referenced `packaging.base` module in them, so we
                                       can't import `pyrin.configuration.services` in this
                                       module. this is more beautiful in comparison to
                                       importing it inside this method.
        """

        flat_configs = config_services.get_all('api')
        application_services.configure(flat_configs)
