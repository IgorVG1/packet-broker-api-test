from enum import Enum


class APIRoutes(str, Enum):
    AUTHENTICATION = '/api/token'
    ADDITIONAL_FILTERS = '/api/additional_filters/'
    BALANCING = '/api/balancing/'
    CUSTOM_CONFIG = '/api/custom_config/'

    def __str__(self):
        return self.value