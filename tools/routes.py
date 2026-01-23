from enum import Enum


class APIRoutes(str, Enum):
    AUTHENTICATION = '/api/token'
    ADDITIONAL_FILTERS = '/api/additional_filters/'
    BALANCING = '/api/balancing/'

    def __str__(self):
        return self.value