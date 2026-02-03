from typing import List, Optional

from pydantic import BaseModel, RootModel, Field, ConfigDict


class LoopbackPortSchema(BaseModel):
    """
    Описание структуры pydantic-model ограничения скорости loopback порта.
    Attributes:
        port: str
        speed_limit (speedLimit): Optional[float]
    """
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    port: str                       = Field(default="L1")
    speed_limit: Optional[float]    = Field(default=10000, alias='speedLimit')


class GetLoopbackPortsResponseSchema(RootModel):
    """
    Описание структуры ответа на получение ограничений скоростей loopback портов.
    Attributes:
        root: List[LoopbackPortSchema] - Список loopback портов с ограничениями скоростей.
    """
    root: List[LoopbackPortSchema]


class CreateLoopbackPortsRequestSchema(RootModel):
    """
    Описание структуры запроса на назначение ограничения скорости loopback портов.
    Attributes:
        root: List[LoopbackPortSchema] - Список loopback портов с ограничениями скоростей.
    """
    root: List[LoopbackPortSchema]  = Field(default=[LoopbackPortSchema()])


class DeleteLoopbackPortsRequestSchema(RootModel):
    """
    Описание структуры запроса на очистку ограничений скоростей loopback портов.
    Attributes:
        root: List[LoopbackPortSchema] - Список loopback портов с ограничениями скоростей.
    """
    root: List[LoopbackPortSchema]  = Field(default=[LoopbackPortSchema()])