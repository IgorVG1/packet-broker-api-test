import allure
from httpx import Response
from requests import Response as requests_Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.loopback_ports.loopback_ports_schema import DeleteLoopbackPortsRequestSchema, CreateLoopbackPortsRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class LoopbackPortsClient(APIClient):
    """
    Клиент для работы с api/loopback_ports/.
    """

    @allure.step('Get loopback ports speed limit list')
    @tracker.track_coverage_httpx(f'{APIRoutes.LOOPBACK_PORTS}')
    def get_loopback_ports_speed(self) -> Response:
        """
        Метод получения ограничений скоростей loopback портов.
        При загрузке страницы http://192.168.7.57/tofino/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.LOOPBACK_PORTS}')


    @allure.step('Create loopback ports speed limit')
    @tracker.track_coverage_httpx(f'{APIRoutes.LOOPBACK_PORTS}')
    def create_loopback_ports(self, request: CreateLoopbackPortsRequestSchema) -> Response:
        """
        Метод назначения ограничения скорости loopback портов.
        При загрузке страницы http://192.168.7.57/tofino/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.LOOPBACK_PORTS}',
                         json=request.model_dump(by_alias=True))


def get_loopback_ports_client(user: AuthenticationUserSchema) -> LoopbackPortsClient:
    """
    Функция создаёт экземпляр LoopbackPortsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию LoopbackPortsClient.
    """
    return LoopbackPortsClient(client=get_private_http_client(user=user))


def get_unauthorised_loopback_ports_client() -> LoopbackPortsClient:
    """
    Функция создаёт экземпляр неавторизованного LoopbackPortsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию LoopbackPortsClient без авторизации.
    """
    return LoopbackPortsClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class LoopbackPortsSession(APISession):

    @allure.step('Delete loopback ports speed limit')
    @tracker.track_coverage_requests(f'{APIRoutes.LOOPBACK_PORTS}')
    def delete_loopback_ports(self, request: DeleteLoopbackPortsRequestSchema) -> requests_Response:
        """
        Метод удаления списка сконфигурированных портов.

        :param request: Словарь DeleteLoopbackPortsRequestSchema.model_dump(by_alias=True).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.LOOPBACK_PORTS}',
                           json=request.model_dump(by_alias=True))


def get_loopback_ports_session(access_token: str) -> LoopbackPortsSession:
    """
    Функция создаёт экземпляр LoopbackPortsSession с уже настроенной HTTP-сессией.

    :return: Готовый к использованию LoopbackPortsSession.
    """
    return LoopbackPortsSession(session=get_private_http_session(access_token=access_token))


def get_unauthorised_loopback_ports_session() -> LoopbackPortsSession:
    """
    Функция создаёт экземпляр неавторизованного LoopbackPortsSession с уже настроенной HTTP-сессией.

    :return: Готовый к использованию LoopbackPortsSession без авторизации.
    """
    return LoopbackPortsSession(session=get_public_http_session())