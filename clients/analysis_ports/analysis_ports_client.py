import allure
from httpx import Response
from requests import Response as requests_Response

from clients.analysis_ports.analysis_ports_schema import CreateAnalysisPortRequestSchema, \
    UpdateAnalysisPortRequestSchema, DeleteAnalysisPortRequestSchema
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.egress_groups.egress_groups_schema import CreateEgressGroupRequestSchema, UpdateEgressGroupRequestSchema, \
    DeleteEgressGroupRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class AnalysisPortsClient(APIClient):
    """
    Клиент для работы с /api/unknown/
    """

    @allure.step('Get analysis ports list')
    @tracker.track_coverage_httpx(f'{APIRoutes.ANALYSIS_PORTS}')
    def get_analysis_port_list_api(self) -> Response:
        """
        Метод получения списка портов анализа.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.ANALYSIS_PORTS}')


    @allure.step('Create analysis port')
    @tracker.track_coverage_httpx(f'{APIRoutes.ANALYSIS_PORTS}')
    def create_analysis_port_api(self, request: CreateAnalysisPortRequestSchema) -> Response:
        """
        Метод добавления порта анализа.

        :param request: Словарь CreateAnalysisPortRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.ANALYSIS_PORTS}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Update analysis port')
    @tracker.track_coverage_httpx(f'{APIRoutes.ANALYSIS_PORTS}')
    def update_analysis_port_api(self, request: UpdateAnalysisPortRequestSchema) -> Response:
        """
        Метод обновления порта анализа.

        :param request: Словарь UpdateAnalysisPortRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.ANALYSIS_PORTS}',
                        json=request.model_dump(by_alias=True))


def get_analysis_ports_client(user: AuthenticationUserSchema) -> AnalysisPortsClient:
    """
    Функция создаёт экземпляр AnalysisPortsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AnalysisPortsClient.
    """
    return AnalysisPortsClient(client=get_private_http_client(user=user))


def get_unauthorised_analysis_ports_client() -> AnalysisPortsClient:
    """
    Функция создаёт экземпляр неавторизованного AnalysisPortsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AnalysisPortsClient без авторизации.
    """
    return AnalysisPortsClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class AnalysisPortsSession(APISession):

    @allure.step('Delete analysis port')
    @tracker.track_coverage_requests(f'{APIRoutes.ANALYSIS_PORTS}')
    def delete_analysis_port_api(self, request: DeleteAnalysisPortRequestSchema) -> requests_Response:
        """
        Метод удаления порта анализа.

        :param request: Словарь DeleteAnalysisPortRequestSchema.model_dump(by_alias=True).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.ANALYSIS_PORTS}',
                           json=request.model_dump(by_alias=True))


def get_analysis_ports_session(access_token: str) -> AnalysisPortsSession:
    """
    Функция создаёт экземпляр AnalysisPortsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AnalysisPortsSession.
    """
    return AnalysisPortsSession(session=get_private_http_session(access_token=access_token))


def get_unauthorised_analysis_ports_session() -> AnalysisPortsSession:
    """
    Функция создаёт экземпляр неавторизованного AnalysisPortsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AnalysisPortsSession без авторизации.
    """
    return AnalysisPortsSession(session=get_public_http_session())