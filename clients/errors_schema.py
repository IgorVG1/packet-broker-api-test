from pydantic import BaseModel


class ValidationErrorResponseSchema(BaseModel):
    """
    Модель, описывающая структуру ответа API с ошибкой валидации.
    Attributes:
        detail: "Учетные данные не были предоставлены."
    """
    detail: str