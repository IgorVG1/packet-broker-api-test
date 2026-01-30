from typing import List

from pydantic import BaseModel, Field, RootModel, ConfigDict


class DataSchema(BaseModel):
    """
    Описание структуры модели сущности data для модели DeleteMirroringRequestSchema.
    Attributes:
        ingress_group (ingressGroup): str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ingress_group: str = Field(alias='ingressGroup', default='ingress-1')


class MirroringSchema(BaseModel):
    """
    Описание структуры модели группы зеркалирования.
    Attributes:
        mirror_id (mirrorId): int
        ports: List[str]
        ingress_id (ingressId): int
        priority: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    mirror_id: int | str      = Field(alias="mirrorId")
    ports: List[str]
    ingress_id: int | str     = Field(alias="ingressId")
    priority: int


class GetMirroringResponseSchema(RootModel):
    """
    Описание структуры ответа на получение групп зеркалирования.
    Attributes:
        root: List[MirroringSchema]
    """
    root: List[MirroringSchema]


class CreateMirroringRequestSchema(BaseModel):
    """
    Описание структуры запроса на добавление группы зеркалирования.
    Attributes:
        id: str
        ingress_group (ingressGroup): str
        ports: List[str]
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    id: str             = Field(default="mirroring-1")
    ingress_group: str  = Field(default="ingress-1", alias="ingressGroup")
    ports: List[str]    = Field(default=["L1"])


class UpdateMirroringRequestSchema(BaseModel):
    """
    Описание структуры запроса на изменение группы зеркалирования.
    Attributes:
        id: str
        ingress_group (ingressGroup): str
        ports: List[str]
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    id: str             = Field(default="mirroring-1")
    ingress_group: str  = Field(default="ingress-1", alias="ingressGroup")
    ports: List[str]    = Field(default=["L2"])


class DeleteMirroringRequestSchema(BaseModel):
    """
    Описание структуры запроса на удаление группы зеркалирования.
    Attributes:
        id: str
        data: DataSchema
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    id: str             = Field(default="mirroring-1")
    data: DataSchema    = Field(default=DataSchema(), description='Вызываем значение по умолчанию: "ingress-1"')