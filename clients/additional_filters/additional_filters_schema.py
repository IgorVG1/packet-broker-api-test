from pydantic import BaseModel, Field, ConfigDict, RootModel
from typing import List


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

    direction: str
    group_id: str   = Field(alias="groupId", serialization_alias="groupId")
    ip: str
    type: str


class CreateAdditionalFiltersRequestSchema(RootModel):
    """
    Описание структуры запроса на создание дополнительных фильтров.
    Attributes:
        List[CreateAdditionalFiltersSchema] - Список дополнительных фильтров

    Модель для запроса, соответствует массиву фильтров.
    Используем __root__ для представления массива верхнего уровня.
    """
    root: List[CreateAdditionalFiltersSchema]

    # Для удобства итерации
    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, index):
        return self.__root__[index]

    def __len__(self):
        return len(self.__root__)

    def model_dump(self, **kwargs):
        """
        Переопределяем, чтобы возвращать список, а не объект с ключом __root__
        """
        # Если запрошен режим JSON или не указан, возвращаем список
        if kwargs.get('mode') == 'json' or not kwargs.get('by_alias'):
            return [item.model_dump(**kwargs) for item in self.__root__]
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs):
        import json
        # Всегда возвращаем JSON-массив
        return json.dumps(self.model_dump(**kwargs))


class CreateAdditionalFiltersResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание дополнительного фильтра.
    """
    pass


class UpdateAdditionalFiltersRequestSchema(BaseModel):
    """
    Описание структуры запроса на сохранение дополнительного фильтра.
    Attributes:
        logic_id: str (logicId)
        filter_ip_white_enable: str (filterIPWhiteEnable)
        filter_ip_black_enable: str (filterIPBlackEnable)
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    logic_id: str                   = Field(alias="logicId", serialization_alias="logicId")
    filter_ip_white_enable: bool    = Field(alias="filterIPWhiteEnable", serialization_alias="filterIPWhiteEnable")
    filter_ip_black_enable: bool    = Field(alias="filterIPBlackEnable", serialization_alias="filterIPBlackEnable")


class UpdateAdditionalFiltersResponseSchema(BaseModel):
    """
    Описание структуры ответа на обновление дополнительного фильтра.
    """
    pass


class DeleteAdditionalFiltersSchema(BaseModel):
    """
    Описание структуры pydantic-model дополнительного фильтра.
    Attributes:
        direction: str
        logic_group: str (logicGroup)
        value: str
        type: str
    """
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)

    direction: str
    logic_group: int = Field(alias="logicGroup", serialization_alias="logicGroup")
    value: str
    type: str


class DeleteAdditionalFiltersRequestSchema(RootModel):
    """
    Описание структуры запроса на удаление дополнительных фильтров.
    Attributes:
        List[DeleteAdditionalFiltersSchema] - Список дополнительных фильтров

    Модель для запроса, соответствует массиву фильтров.
    Используем __root__ для представления массива верхнего уровня.
    """
    root: List[DeleteAdditionalFiltersSchema]

    # Для удобства итерации
    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, index):
        return self.__root__[index]

    def __len__(self):
        return len(self.__root__)

    def model_dump(self, **kwargs):
        """
        Переопределяем, чтобы возвращать список, а не объект с ключом __root__
        """
        # Если запрошен режим JSON или не указан, возвращаем список
        if kwargs.get('mode') == 'json' or not kwargs.get('by_alias'):
            return [item.model_dump(**kwargs) for item in self.__root__]
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs):
        import json
        # Всегда возвращаем JSON-массив
        return json.dumps(self.model_dump(**kwargs))