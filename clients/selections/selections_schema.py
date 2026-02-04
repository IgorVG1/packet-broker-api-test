from typing import List

from pydantic import BaseModel, Field, RootModel, ConfigDict


class GetSelectionSchema(BaseModel):
    """
    Описание структуры pydantic-model группы отбора в ответе запроса на получение.
    Attributes:
        logic_id (logicId): int
        ingress_id (ingressId): int
        ip_protocol (ipProtocol): int
        src_port (srcPort): int
        dst_port (dstPort): int
        traffic_type (trafficType): int
        match_priority (matchPriority): int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_id: int       = Field(alias="logicId")
    ingress_id: int     = Field(alias="ingressId")
    ip_protocol: int    = Field(alias='ipProtocol')
    src_port: int       = Field(alias='srcPort')
    dst_port: int       = Field(alias='dstPort')
    traffic_type: int   = Field(alias='trafficType')
    match_priority: int = Field(alias='matchPriority')


class GetSelectionsResponseSchema(RootModel):
    """
    Описание структуры ответа на получение списка групп отбора.
    Attributes:
        root: List[GetSelectionSchema]
    """
    root: List[GetSelectionSchema]


class CreateSelectionSchema(BaseModel):
    """
    Описание структуры pydantic-model группы отбора в ответе запроса на создание.
    Attributes:
        ip_protocol (ipProtocol): int
        traffic_type (trafficType): int
        src_port (srcPort): int
        dst_port (dstPort): int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ip_protocol: int    = Field(default=0, alias='ipProtocol')
    traffic_type: int   = Field(default=0, alias='trafficType')
    src_port: int       = Field(default=0, alias='srcPort')
    dst_port: int       = Field(default=0, alias='dstPort')


class CreateSelectionRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание группы отбора.
    Attributes:
        ingress_id (ingressId): str
        logic_id (logicId): str
        selection: SelectionSchema
        match_priority (matchPriority): int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ingress_id: str             = Field(default="ingress-9", alias='ingressId')
    logic_id: str               = Field(default="selection-9", alias='logicId')
    selection: CreateSelectionSchema  = Field(default=CreateSelectionSchema())
    match_priority: int         = Field(default=0, alias='matchPriority')


class FilterSchema(BaseModel):
    """
    Описание структуры pydantic-model фильтра в группе отбора.
    Attributes:
        ip_protocol (ipProtocol): int
        traffic_type (trafficType): int
        src_port (srcPort): int
        dst_port (dstPort): int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ip_protocol: int    = Field(default=0, alias='ipProtocol')
    traffic_type: int   = Field(default=0, alias='trafficType')
    src_port: int       = Field(default=0, alias='srcPort')
    dst_port: int       = Field(default=0, alias='dstPort')


class DeleteSelectionRequestSchema(BaseModel):
    """
    Описание структуры запроса на удаление группы отбора.
    Attributes:
        ingress_group (ingressGroup): str
        filter: FilterSchema
        match_priority (matchPriority): int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ingress_group: str      = Field(default="ingress-9", alias='ingressGroup')
    filter: FilterSchema    = Field(default=FilterSchema())
    match_priority: int     = Field(default=0, alias='matchPriority')