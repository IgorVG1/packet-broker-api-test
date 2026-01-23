from pydantic import BaseModel, Field, ConfigDict, RootModel
from typing import List
from tools.fakers import fake


class BalancingListSchema(BaseModel):
    """
    Описание структуры pydantic-model балансировки группы.
    Attributes:
        logic_id: int (logicId)
        sel: int
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_id: int = Field(alias="logicId")
    sel: int


class GetBalancingListResponseSchema(RootModel):
    """
    Описание структуры запроса на создание балансировок групп.
    Attributes:
        List[BalancingListSchema] - Список балансировок групп
    """
    root: List[BalancingListSchema]


class CreateBalancingRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание балансировки группы.
    Attributes:
        logic_id: int (logicId)
        balance_type: int (balanceType)
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_id: int | str     = Field(alias="logicId", default=1)
    balance_type: int | str = Field(alias="balanceType", default=1)


class UpdateBalancingRequestSchema(BaseModel):
    """
    Описание структуры запроса на редактирование конфигурации группы балансировки.
    Attributes:
        logic_id: int (logicId)
        balance_type: int (balanceType)
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_id: int | str     = Field(alias="logicId", default=1)
    balance_type: int | str = Field(alias="balanceType", default=1)


class DeleteBalancingRequestSchema(BaseModel):
    """
    Описание структуры pydantic-model для запроса на удаление балансировки.
    Attributes:
        value: str
        direction: str
        logicGroup: int
        type: str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_group: int = Field(alias="logicGroup", default=1)