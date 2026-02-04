from typing import List
from tools.fakers import fake
from pydantic import BaseModel, Field, RootModel, ConfigDict


class ConfiguredPortSchema(BaseModel):
    """
    Описание структуры pydantic-model порта.
    Attributes:
        port: str
        speed: str
        mtu: int
        an: str
        fec: str
        dir: str
        up: bool
        enable: bool
        monitoring: int
        action: int
        loopback: str
        reserve_port (reservePort): Optional[str]
        mac_dst_egress (macDstEgress): Optional[str]
        name: str
        pid: int
        lid: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    port: str | None
    speed: str | None
    mtu: int | None
    an: str | None
    fec: str | None
    dir: str | None
    up: bool | None
    enable: bool | None
    monitoring: int | None
    action: int | None
    loopback: str | None
    reserve_port: str | None    = Field(alias='reservePort')
    mac_dst_egress: str | None  = Field(alias='macDstEgress')
    name: str | None
    pid: int | None
    lid: int | None


class UpdatedPortSchema(BaseModel):
    """
    Описание структуры примера запроса на обновление сконфигурированного порта.
    Attributes:
        name: str (генерируется случайным образом на основе случайных цветов)
        port: str
        speed: str
        mtu: int
        an: str
        fec: str
        dir: str
        speed_limit (speedLimit): int
        loopback: str
        reserve_port (reservePort): str
        reserve_port_mode (reservePortMode): str
        mac_dst_egress (macDstEgress): str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    name: str               = Field(default_factory=fake.port_name)
    port: str               = Field(default='1/0')
    speed: str              = Field(default='BF_SPEED_100G')
    mtu: int                = Field(default=10240)
    an: str                 = Field(default='PM_AN_FORCE_ENABLE')
    fec: str                = Field(default='BF_FEC_TYP_NONE')
    dir: str                = Field(default='PM_PORT_DIR_DEFAULT')
    speed_limit: int        = Field(default=102400, alias='speedLimit')
    loopback: str           = Field(default='BF_LPBK_NONE')
    reserve_port: str|None  = Field(default=None, alias='ReservePort')
    reserve_port_mode: str  = Field(default='overflow', alias='reservePortMode')
    mac_dst_egress: str     = Field(default='08bfb8003489', alias='macDstEgress')


class GetPortsListResponse(RootModel):
    """
    Описание структуры ответа на получение списка сконфигурированных портов.
    Attributes:
        root: List[ConfiguredPortSchema] - Список сконфигурированных портов.
    """
    root: List[ConfiguredPortSchema]


class GetPossiblePortsListResponse(RootModel):
    """
    Описание структуры ответа на получение списка доступных портов.
    Attributes:
        root: List[str] - Список доступных портов.
    """
    root: List[str]


class CreatePortRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание сконфигурированного порта.
    Attributes:
        name: str
        port: str
        speed: str
        mtu: int
        an: str
        fec: str
        dir: str
        speed_limit (speedLimit): int
        loopback: str
        reserve_port (reservePort): str
        reserve_port_mode (reservePortMode): str
        mac_dst_egress (macDstEgress): str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    name: str               = Field(default='test_name')
    port: str               = Field(default='1/0')
    speed: str              = Field(default='BF_SPEED_100G')
    mtu: int                = Field(default=10240)
    an: str                 = Field(default='PM_AN_FORCE_ENABLE')
    fec: str                = Field(default='BF_FEC_TYP_NONE')
    dir: str                = Field(default='PM_PORT_DIR_DEFAULT')
    speed_limit: int        = Field(default=102400, alias='speedLimit')
    loopback: str           = Field(default='BF_LPBK_NONE')
    reserve_port: str|None  = Field(default=None, alias='reservePort')
    reserve_port_mode: str  = Field(default='overflow', alias='reservePortMode')
    mac_dst_egress: str     = Field(default='08bfb8003489', alias='macDstEgress')


class CreatePortRequest412Schema(BaseModel):
    """
    Описание структуры запроса на создание сконфигурированного порта для вызова ошибки 412.
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    name: str               = Field(default="412")


class DeletePortsRequestSchema(RootModel):
    """
    Описание структуры ответа на удаление списка указанных портов.
    Attributes:
        root: List[str] - Список сконфигурированных портов.
    """
    root: List[str] = Field(default=["1/0"])