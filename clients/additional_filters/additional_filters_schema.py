from pydantic import BaseModel, Field, ConfigDict, RootModel
from typing import List, Optional
from tools.fakers import fake


class CreateAdditionalFiltersSchema(BaseModel):
    """
    Описание структуры pydantic-model дополнительного фильтра.
    Attributes:
        direction: str
        group_id: str (groupId)
        ip: str
        type: str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    direction: str  = Field(default="Src+Dst")
    group_id: str   = Field(alias="groupId", serialization_alias="groupId", default="1")
    ip: str         = Field(default_factory=fake.ip)
    type: str       = Field(default="pass")


class CreateAdditionalFiltersRequestSchema(RootModel):
    """
    Описание структуры запроса на создание дополнительных фильтров.
    Attributes:
        List[CreateAdditionalFiltersSchema] - Список дополнительных фильтров
    """
    root: List[CreateAdditionalFiltersSchema]


class UpdateAdditionalFiltersRequestSchema(BaseModel):
    """
    Описание структуры запроса на сохранение дополнительного фильтра.
    Attributes:
        logic_id: str (logicId)
        filter_ip_white_enable: str (filterIPWhiteEnable)
        filter_ip_black_enable: str (filterIPBlackEnable)
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_id: str                   = Field(alias="logicId", serialization_alias="logicId", default='1')
    filter_ip_white_enable: bool    = Field(alias="filterIPWhiteEnable", serialization_alias="filterIPWhiteEnable", default_factory=fake.boolean)
    filter_ip_black_enable: bool    = Field(alias="filterIPBlackEnable", serialization_alias="filterIPBlackEnable", default_factory=fake.boolean)


class DeleteAdditionalFiltersSchema(BaseModel):
    """
    Описание структуры pydantic-model для запроса на удаление дополнительного фильтра.
    Attributes:
        value: str
        direction: str
        logicGroup: int
        type: str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    value: Optional[str]       = Field(default="1.1.1.1")
    direction: Optional[str]   = Field(default="Src+Dst")
    logic_group: Optional[int] = Field(alias="logicGroup", default=1)
    type: Optional[str]        = Field(default="pass")


class DeleteAdditionalFiltersRequestSchema(RootModel):
    """
    Описание структуры запроса на удаление дополнительных фильтров.
    Attributes:
        List[DeleteAdditionalFiltersSchema] - Список дополнительных фильтров
    """
    root: List[DeleteAdditionalFiltersSchema]