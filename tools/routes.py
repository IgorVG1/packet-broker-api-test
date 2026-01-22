from enum import Enum


class APIRoutes(str, Enum):
    AUTHENTICATION = '/api/token'
    ADDITIONAL_FILTERS = '/api/additional_filters/'