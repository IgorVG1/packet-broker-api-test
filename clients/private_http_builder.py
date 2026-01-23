from functools import lru_cache

from httpx import Client
from pydantic import BaseModel, ConfigDict, Field
from requests import Session

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.event_hooks import log_request_event_hook, log_response_event_hook
from config import settings


class AuthenticationUserSchema(BaseModel):
    """
    Структура данных пользователя для авторизации
    Attributes:
        username: str
        password: str
    """
    model_config = ConfigDict(frozen=True)

    username: str   = Field(default=settings.user_data.username)
    password: str   = Field(default=settings.user_data.password)


@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    :param user: Объект AuthenticationUserSchema с username и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """
    authentication_client = get_authentication_client()
    login_request = LoginRequestSchema(username=user.username,
                                       password=user.password)
    login_response = authentication_client.login(request=login_request)

    return Client(
        event_hooks={"request": [log_request_event_hook],
                     "response": [log_response_event_hook]},
        base_url=settings.http_client.client_url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {login_response.access}"}
    )


@lru_cache(maxsize=None)
def get_private_http_session(access_token: str) -> Session:
    """
    Функция создаёт экземпляр requests.Session с аутентификацией пользователя.

    :param access_token: Строковое значение access-token.
    :return: Готовый к использованию объект requests.Session с установленным заголовком Authorization.
    """
    session = Session()
    session.headers = {"Authorization": f"Bearer {access_token}"}
    return session