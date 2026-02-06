from typing import List

from pydantic import BaseModel, RootModel, Field


class PsfFormatSchema(BaseModel):
    """
    Описание структуры pydantic-model правила спецформата.
    Attributes:
        port: str
        dmac: str
        lid: int
        pid: int
    """
    port: str
    dmac: str
    lid: int | None
    pid: int | None


class GetPsfFormatResponseSchema(RootModel):
    """
    Описание структуры ответа на получение списка правил спецформата.
    Attributes:
        root: List[PsfFormatSchema] - Список правил спецформата.
    """
    root: List[PsfFormatSchema]


class CreatePsfFormatRequestSchema(BaseModel):
    """
    Описание структуры запроса на добавление правила спецформата.
    Attributes:
        port: str
        dmac: str
        lid: str
        pid: str
    """

    port: str       = Field(default='L2')
    dmac: str       = Field(default='112233445566')
    lid: str | None = Field(default=None)
    pid: str | None = Field(default=None)


class UpdatePsfFormatRequestSchema(BaseModel):
    """
    Описание структуры запроса на изменение правила спецформата.
    Attributes:
        port: str
        dmac: str
        lid: str
        pid: str
    """

    port: str       = Field(default='L2')
    dmac: str       = Field(default='665544332211')
    lid: str | None = Field(default=None)
    pid: str | None = Field(default=None)


class DeletePsfFormatRequestSchema(RootModel):
    """
    Описание структуры запроса на удаление правила спецформата.
    Attributes:
        root: List[str]
    """

    root: List[str] = Field(default=['L2'])