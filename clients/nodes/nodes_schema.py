from typing import List, Any, Optional

from pydantic import BaseModel, Field, ConfigDict


class PositionSchema(BaseModel):
    """
    Описание структуры pydantic-model позиции ноды.
    Attributes:
        x: float
        y: float
    """

    x: float
    y: float


class ViewportSchema(BaseModel):
    """
    Описание структуры pydantic-model области видимости конфигурации на Web.
    Attributes:
        x: float
        y: float
        zoom: float
    """
    x: float    = Field(default=250)
    y: float    = Field(default=25)
    zoom: float = Field(default=0.6)

#-----------------------------------------------------------------------------------------------------------------------

class DataIngressGroupSchema(BaseModel):
    """
    Описание структуры pydantic-model данных ноды входной группы.
    Attributes:
        ports: List[Any]
        logic_group (logicGroup): List[str]
        counter: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ports: List[Any]        = Field(default=[])
    logic_group: List[str]  = Field(default=['selection-1'], alias="logicGroup")
    counter: int            = Field(default=0)


class NodeIngressGroupSchema(BaseModel):
    """
    Описание структуры pydantic-model ноды входной группы.
    Attributes:
        id: str
        type: str
        data: DataIngressGroupSchema
        position: PositionSchema
    """
    id: str                         = Field(default="ingress-1")
    type: str                       = Field(default='ingress')
    data: DataIngressGroupSchema    = Field(default=DataIngressGroupSchema())
    position: PositionSchema        = Field(default=PositionSchema(x=0, y=0))

#-----------------------------------------------------------------------------------------------------------------------

class FilterDataSelectionSchema(BaseModel):
    """
    Описание структуры pydantic-model фильтра данных ноды группы отбора.
    Attributes:
        ip_protocol (ipProtocol): Optional[Any]
        src_port (srcPort): Optional[Any]
        dst_port (dstPort): Optional[Any]
        traffic_type (trafficType): float
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ip_protocol: Optional[Any]  = Field(default=None, alias="ipProtocol")
    src_port: Optional[Any]     = Field(default=None, alias="srcPort")
    dst_port: Optional[Any]     = Field(default=None, alias="dstPort")
    traffic_type: float         = Field(default=0, alias="trafficType")


class DataSelectionSchema(BaseModel):
    """
    Описание структуры pydantic-model данных ноды группы отбора.
    Attributes:
        ingress_group (ingressGroup): str
        filter: FilterDataSelectionSchema
        match_priority (matchPriority): float
        counter: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ingress_group: str                  = Field(default='ingress-1', alias="ingressGroup")
    filter: FilterDataSelectionSchema   = Field(default=FilterDataSelectionSchema())
    match_priority: float               = Field(default=0, alias="matchPriority")
    counter: int                        = Field(default=0)


class NodeSelectionSchema(BaseModel):
    """
    Описание структуры pydantic-model ноды группы отбора.
    Attributes:
        id: str
        type: str
        data: DataSelectionSchema
        position: PositionSchema
    """
    id: str                     = Field(default="selection-1")
    type: str                   = Field(default='selection')
    data: DataSelectionSchema   = Field(default=DataIngressGroupSchema())
    position: PositionSchema    = Field(default=PositionSchema(x=300, y=0))

#-----------------------------------------------------------------------------------------------------------------------

class DataBalancingSchema(BaseModel):
    """
    Описание структуры pydantic-model данных ноды балансировки.
    Attributes:
        logic_group (logicGroup): str
        balancing_type (balancingType): Optional[Any]
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_group: str                = Field(default='selection-1', alias="logicGroup")
    balancing_type: Optional[Any]   = Field(default=None, alias="balancingType")


class NodeBalancingSchema(BaseModel):
    """
    Описание структуры pydantic-model ноды балансировки.
    Attributes:
        id: str
        type: str
        data: DataSelectionSchema
        position: PositionSchema
    """
    id: str                     = Field(default="balancing-1")
    type: str                   = Field(default='balancing')
    data: DataBalancingSchema   = Field(default=DataBalancingSchema())
    position: PositionSchema    = Field(default=PositionSchema(x=700, y=0))

#-----------------------------------------------------------------------------------------------------------------------

class DataFiltrationSchema(BaseModel):
    """
    Описание структуры pydantic-model данных ноды фильтрации.
    Attributes:
        logic_group (logicGroup): str
        counter: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_group: str    = Field(default='selection-1', alias="logicGroup")
    counter: int        = Field(default=0)


class NodeFiltrationSchema(BaseModel):
    """
    Описание структуры pydantic-model ноды фильтрации.
    Attributes:
        id: str
        type: str
        data: DataFiltrationSchema
        position: PositionSchema
    """
    id: str                     = Field(default="filtration-1")
    type: str                   = Field(default='filtration')
    data: DataFiltrationSchema   = Field(default=DataFiltrationSchema())
    position: PositionSchema    = Field(default=PositionSchema(x=1250, y=0))

#-----------------------------------------------------------------------------------------------------------------------

class DataEgressGroupSchema(BaseModel):
    """
    Описание структуры pydantic-model данных ноды выходной группы.
    Attributes:
        ports: List[Any]
        logic_group (logicGroup): List[str]
        counter: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ports: List[Any]        = Field(default=[])
    logic_group: List[str]  = Field(default=['selection-1'], alias="logicGroup")
    counter: int            = Field(default=0)


class NodeEgressGroupSchema(BaseModel):
    """
    Описание структуры pydantic-model ноды выходной группы.
    Attributes:
        id: str
        type: str
        data: DataEgressGroupSchema
        position: PositionSchema
    """
    id: str                     = Field(default="egress-1")
    type: str                   = Field(default='egress')
    data: DataEgressGroupSchema = Field(default=DataEgressGroupSchema())
    position: PositionSchema    = Field(default=PositionSchema(x=1600, y=0))

#-----------------------------------------------------------------------------------------------------------------------

class DataMirroringSchema(BaseModel):
    """
    Описание структуры pydantic-model данных ноды группы зеркалирования.
    Attributes:
        ports: List[Any]
        ingress_group (ingressGroup): List[str]
        priority: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ports: List[Any]            = Field(default=[])
    ingress_group: List[str]    = Field(default=['ingress-1'], alias="ingressGroup")
    priority: int               = Field(default=0)


class NodeMirroringSchema(BaseModel):
    """
    Описание структуры pydantic-model ноды группы зеркалирования.
    Attributes:
        id: str
        type: str
        data: DataMirroringSchema
        position: PositionSchema
    """
    id: str                     = Field(default="mirroring-1")
    type: str                   = Field(default='mirror')
    data: DataMirroringSchema   = Field(default=DataMirroringSchema())
    position: PositionSchema    = Field(default=PositionSchema(x=300, y=350))

#-----------------------------------------------------------------------------------------------------------------------

class DataAnalysisSchema(BaseModel):
    """
    Описание структуры pydantic-model данных ноды порта анализа.
    Attributes:
        ports: List[Any]
        ingress_group (ingressGroup): List[str]
        counter: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    ports: List[Any]            = Field(default=[])
    ingress_group: List[str]    = Field(default=['ingress-1'], alias="ingressGroup")
    counter: int                = Field(default=0)


class NodeAnalysisSchema(BaseModel):
    """
    Описание структуры pydantic-model ноды порта анализа.
    Attributes:
        id: str
        type: str
        data: DataAnalysisSchema
        position: PositionSchema
    """
    id: str                     = Field(default="unknown-1")
    type: str                   = Field(default='unknown')
    data: DataAnalysisSchema    = Field(default=DataMirroringSchema())
    position: PositionSchema    = Field(default=PositionSchema(x=300, y=600))

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

class CreateNodesRequestSchema(BaseModel):
    """
    Описание структуры запроса на сохранение текущей конфигурации c Web.
    Attributes:
        nodes: List[Node*Schema]
        edges: List[Any]
        position: List[float]
        zoom: float
        viewport: ViewportSchema
    """
    nodes: List[Any]            = Field(default=[
                                                    NodeIngressGroupSchema(),
                                                    NodeSelectionSchema(),
                                                    NodeBalancingSchema(),
                                                    NodeFiltrationSchema(),
                                                    NodeEgressGroupSchema(),
                                                    NodeMirroringSchema(),
                                                    NodeAnalysisSchema()])
    edges: List[Any]            = Field(default=[])
    position: List[float]       = Field(default=[250, 25])
    zoom: float                 = Field(default=0.6)
    viewport: ViewportSchema    = Field(default=ViewportSchema())