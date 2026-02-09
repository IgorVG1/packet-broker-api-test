from enum import Enum


class APIRoutes(str, Enum):
    AUTHENTICATION = '/api/token'
    ADDITIONAL_FILTERS = '/api/additional_filters/'
    BALANCING = '/api/balancing/'
    CUSTOM_CONFIG = '/api/custom_config/'
    DEFAULT_CONFIG = '/api/default_config/'
    FILTERS = '/api/filters/'
    ALL_FILTERS = '/api/all_filters/'
    MIRRORING = '/api/mirroring/'
    PORTS = '/api/ports/'
    PORTS_ALL = '/api/ports_all/'
    PORT_STATUS = '/api/port_status/'
    LOOPBACK_PORTS = '/api/loopback_ports/'
    INGRESS_GROUPS = '/api/ingress_groups/'
    NODES = '/api/nodes/'
    SELECTIONS = '/api/selections/'
    SWITCH_INFO = '/api/switch_info/'
    EGRESS_GROUPS = '/api/egress_groups/'
    ANALYSIS_PORTS = '/api/unknown/'
    PSF_FORMAT = '/api/psf_format/'
    PSF_DMAC = '/api/psf_dmac/'
    MIRROR_FILTER = '/api/mirror_filter/'
    PSF_MIRROR_FILTER = '/api/psf_mirror_filter/'

    def __str__(self):
        return self.value