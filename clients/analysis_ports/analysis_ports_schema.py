from typing import List

from pydantic import BaseModel, RootModel, Field, ConfigDict


class DataSchema(BaseModel):
    """
    Описание структуры атрибута данных в модели DeleteAnalysisPortRequestSchema.
    Attributes:
        ingress_group (ingressGroup): str
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    ingress_group: str = Field(default="ingress-2", alias="ingressGroup")


class AnalysisPortSchema(BaseModel):
    """
    Описание структуры pydantic-model порта анализа.
    Attributes:
        ingress_id (ingressId): int
        egress_port (egressPort): str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ingress_id: int     = Field(alias='ingressId')
    egress_port: str    = Field(alias='egressPort')


class GetAnalysisPortsResponseSchema(RootModel):
    """
    Описание структуры ответа на получение списка портов анализа.
    Attributes:
        root: List[AnalysisPortSchema] - Список портов анализа.
    """
    root: List[AnalysisPortSchema]


class CreateAnalysisPortRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание группы анализа.
    Attributes:
        id (groupId): str
        ingress_group (ingressGroup): str
        ports: List[str]
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: str             = Field(default='unknown-1')
    ingress_group: str  = Field(default='ingress-2', alias='ingressGroup')
    ports: List[str]    = Field(default=['L1'])


class UpdateAnalysisPortRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление порта анализа.
    Attributes:
        id (groupId): str
        ingress_group (ingressGroup): str
        ports: List[str]
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: str             = Field(default='unknown-1')
    ingress_group: str  = Field(default='ingress-2', alias='ingressGroup')
    ports: List[str]    = Field(default=['L2'])


class DeleteAnalysisPortRequestSchema(BaseModel):
    """
    Описание структуры запроса на удаление порта анализа.
    Attributes:
        id (groupId): str
        data:
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    id: str             = Field(default='unknown-1')
    data: DataSchema    = Field(default=DataSchema())