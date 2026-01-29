from pydantic import BaseModel


class AuthenticationErrorResponseSchema(BaseModel):
    """
    Модель, описывающая структуру ответа API с ошибкой аутентификации пользователя.
    Attributes:
        detail: "Учетные данные не были предоставлены."
    """
    detail: str