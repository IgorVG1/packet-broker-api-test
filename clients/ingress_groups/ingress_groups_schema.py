from typing import List

from pydantic import BaseModel, RootModel, Field, ConfigDict


class PortSchema(BaseModel):
    """
    Описание структуры pydantic-model порта.
    Attributes:
        port: str
    """
    port: str = Field(default="L1")


class IngressGroupSchema(BaseModel):
    """
    Описание структуры pydantic-model входной группы.
    Attributes:
        id: int
        ports: List[str]
        packet_counter (packetCounter): List[int]
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: int
    ports: List[str]
    packet_counter: List[int]   = Field(alias='packetCounter')


class GetIngressGroupsResponseSchema(RootModel):
    """
    Описание структуры ответа на получение списка входных групп.
    Attributes:
        root: List[LoopbackPortSchema] - Список loopback портов с ограничениями скоростей.
    """
    root: List[IngressGroupSchema]


class CreateIngressGroupRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание выходной группы.
    Attributes:
        group_id (groupId): str
        ports: List[PortSchema]
    """
    group_id: str           = Field(default='ingress-2', alias='groupId')
    ports: List[PortSchema] = Field(default=[PortSchema()])


class UpdateIngressGroupRequestSchema(BaseModel):
    """
    Описание структуры запроса на изменение выходной группы.
    Attributes:
        group_id (groupId): str
        ports: List[PortSchema]
    """
    group_id: str           = Field(default='ingress-2', alias='groupId')
    ports: List[PortSchema] = Field(default=[PortSchema(port="L1")])


class DeleteIngressGroupRequestSchema(BaseModel):
    """
    Описание структуры запроса на удаление выходной группы.
    Attributes:
        group_id (groupId): str
        ports: List[PortSchema]
    """
    group_id: str           = Field(default='ingress-2', alias='groupId')
    ports: List[PortSchema] = Field(default=[PortSchema()])