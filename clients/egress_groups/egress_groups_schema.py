from typing import List

from pydantic import BaseModel, RootModel, Field, ConfigDict


class DataSchema(BaseModel):
    """
    Описание структуры атрибута данных в модели DeleteEgressGroupRequestSchema.
    Attributes:
        logic_group (logicGroup): str
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    logic_group: str = Field(default="selection-9", alias="logicGroup")


class PortSchema(BaseModel):
    """
    Описание структуры pydantic-model порта.
    Attributes:
        port: str
    """
    port: str = Field(default="L1")


class EgressGroupSchema(BaseModel):
    """
    Описание структуры pydantic-model выходной группы.
    Attributes:
        ports: List[str]
        logic_group (logicGroup): int
        group_id (groupId): int
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    ports: List[str]
    logic_group: int    = Field(alias="logicGroup")
    group_id: int       = Field(alias='groupId')


class GetEgressGroupsResponseSchema(RootModel):
    """
    Описание структуры ответа на получение списка выходных групп.
    Attributes:
        root: List[EgressGroupSchema] - Список выходных групп.
    """
    root: List[EgressGroupSchema]


class CreateEgressGroupRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание выходной группы.
    Attributes:
        group_id (groupId): str
        logic_group (logicGroup): str
        ports: List[PortSchema]
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    group_id: str           = Field(default='egress-9', alias='groupId')
    logic_group: str        = Field(default='selection-9', alias='logicGroup')
    ports: List[PortSchema] = Field(default=[PortSchema()])


class UpdateEgressGroupRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление выходной группы.
    Attributes:
        group_id (groupId): str
        logic_group (logicGroup): str
        ports: List[PortSchema]
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    group_id: str           = Field(default='egress-1', alias='groupId')
    logic_group: str        = Field(default='selection-1', alias='logicGroup')
    ports: List[PortSchema] = Field(default=[PortSchema(port="L2")])


class DeleteEgressGroupRequestSchema(BaseModel):
    """
    Описание структуры запроса на удаление выходной группы.
    Attributes:
        id: str
        data: DataSchema
    """
    id: str             = Field(default='egress-9')
    data: DataSchema    = Field(default=DataSchema())