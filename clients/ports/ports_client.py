import allure
from httpx import Response
from requests import Response as requests_Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.ports.ports_schema import CreatePortRequestSchema, DeletePortsRequestSchema, UpdatedPortSchema, \
    UpdatePortStatusRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class PortsClient(APIClient):
    """
    Клиент для работы с /api/ports/
    """
    @allure.step('Get configured ports list')
    @tracker.track_coverage_httpx(f'{APIRoutes.PORTS}')
    def get_ports_list_api(self) -> Response:
        """
        Метод получения списка сконфигурированных портов и их настроек.
        При загрузке страницы http://192.168.7.57/tofino/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.PORTS}')


    @allure.step('Get possible ports list')
    @tracker.track_coverage_httpx(f'{APIRoutes.PORTS}')
    def get_possible_ports_list_api(self) -> Response:
        """
        Метод получения списка возможных портов.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.options(url=f'{APIRoutes.PORTS}')


    @allure.step('Create configured port')
    @tracker.track_coverage_httpx(f'{APIRoutes.PORTS}')
    def create_ports_api(self, request: CreatePortRequestSchema) -> Response:
        """
        Метод конфигурации нового порта.

        :param request: Словарь CreatePortRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.PORTS}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Update configured ports')
    @tracker.track_coverage_httpx(f'{APIRoutes.PORTS}')
    def update_ports_api(self, request: UpdatedPortSchema) -> Response:
        """
        Метод обновления порта.

        :param request: Словарь UpdatePortRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.PORTS}',
                        json=[request.model_dump(by_alias=True)])




    @allure.step('Update status port')
    @tracker.track_coverage_httpx(f'{APIRoutes.PORT_STATUS}')
    def update_port_status_api(self, request: UpdatePortStatusRequestSchema) -> Response:
        """
        Метод изменения состояния порта.

        :param request: Словарь UpdatePortStatusRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.PORT_STATUS}',
                        json=request.model_dump())




    @allure.step('Get all ports list')
    @tracker.track_coverage_httpx(f'{APIRoutes.PORTS_ALL}')
    def get_all_ports_list_api(self) -> Response:
        """
        Метод вывода списка всех доступных портов с информацией о модулях.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.PORTS_ALL}')


def get_ports_client(user: AuthenticationUserSchema) -> PortsClient:
    """
    Функция создаёт экземпляр PortsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PortsClient.
    """
    return PortsClient(client=get_private_http_client(user=user))


def get_unauthorised_ports_client() -> PortsClient:
    """
    Функция создаёт экземпляр неавторизованного PortsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PortsClient без авторизации.
    """
    return PortsClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class PortsSession(APISession):

    @allure.step('Delete configured ports')
    @tracker.track_coverage_requests(f'{APIRoutes.PORTS}')
    def delete_ports_api(self, request: DeletePortsRequestSchema) -> requests_Response:
        """
        Метод удаления списка сконфигурированных портов.

        :param request: Словарь DeletePortsRequestSchema.model_dump(by_alias=True).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.PORTS}',
                           json=request.model_dump(by_alias=True))


    @allure.step('Delete nonexistent ports')
    @tracker.track_coverage_requests(f'{APIRoutes.PORTS}')
    def incorrect_delete_ports_api(self) -> requests_Response:
        """
        Метод для обработки ошибки [412] с помощью удаления не существующего порта.

        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.PORTS}')


def get_ports_session(access_token: str) -> PortsSession:
    """
    Функция создаёт экземпляр PortsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PortsSession.
    """
    return PortsSession(session=get_private_http_session(access_token=access_token))


def get_unauthorised_ports_session() -> PortsSession:
    """
    Функция создаёт экземпляр неавторизованного PortsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PortsSession без авторизации.
    """
    return PortsSession(session=get_public_http_session())