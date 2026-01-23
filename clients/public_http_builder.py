from httpx import Client
from requests import Session

from clients.event_hooks import log_request_event_hook, log_response_event_hook
from config import settings


def get_public_http_client() -> Client:
    """
    Функция создаёт экземпляр httpx.Client с базовыми настройками.

    :return: Готовый к использованию объект httpx.Client.
    """
    return Client(
        event_hooks={"request": [log_request_event_hook],
                     "response": [log_response_event_hook]},
        base_url=settings.http_client.client_url,
        timeout=settings.http_client.timeout
    )

def get_public_http_session() -> Session:
    """
    Функция создаёт экземпляр requests.Session с базовыми настройками.

    :return: Готовый к использованию объект requests.Session.
    """
    return Session()