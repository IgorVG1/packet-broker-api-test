import allure
from httpx import Response
from requests import Response as requests_Response
from clients.balancing.balancing_schema import GetBalancingListResponseSchema, CreateBalancingRequestSchema, \
    UpdateBalancingRequestSchema, DeleteBalancingRequestSchema
from clients.api_client import APIClient
from clients.api_session import APISession
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client, get_private_http_session
from config import settings
from tools.routes import APIRoutes
from clients.api_coverage import tracker

# ----------------------------------------------------------------------------------------------------------------------

class BalancingClient(APIClient):
    """
    Клиент для работы с /api/balancing/
    """
    @allure.step('Get balancing list')
    @tracker.track_coverage_httpx(f'{APIRoutes.BALANCING}')
    def get_balancing_list_api(self) -> Response:
        """
        Метод получения списка сконфигурированных групп балансировки.

        :return: Ответ от сервера.
        """
        return self.get(url=f'{APIRoutes.BALANCING}')

    def get_balancing_list(self) -> GetBalancingListResponseSchema:
        response = self.get_balancing_list_api()
        return GetBalancingListResponseSchema.model_validate_json(response.text)


    @allure.step('Create balancing group')
    @tracker.track_coverage_httpx(f'{APIRoutes.BALANCING}')
    def create_balancing_api(self, request: CreateBalancingRequestSchema) -> Response:
        """
        Метод конфигурирования группы балансировки.

        :param request: Словарь с logic_id(logicId), balance_type(balanceType).
        :return: Ответ от сервера.
        """
        return self.post(url=f'{APIRoutes.BALANCING}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Update balancing group')
    @tracker.track_coverage_httpx(f'{APIRoutes.BALANCING}')
    def update_balancing_api(self, request: UpdateBalancingRequestSchema) -> Response:
        """
        Метод редактирования конфигурации группы балансировки.

        :param request: Словарь с logic_id(logicId), balance_type(balanceType).
        :return: Ответ от сервера.
        """
        return self.put(url=f'{APIRoutes.BALANCING}',
                        json=request.model_dump(by_alias=True))


def get_balancing_client(user: AuthenticationUserSchema) -> BalancingClient:
    """
    Функция создаёт экземпляр BalancingClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию BalancingClient.
    """
    return BalancingClient(client=get_private_http_client(user=user))

# ----------------------------------------------------------------------------------------------------------------------

class BalancingSession(APISession):

    @allure.step('Delete balancing group')
    @tracker.track_coverage_requests(f'{APIRoutes.BALANCING}')
    def delete_balancing_api(self, request: DeleteBalancingRequestSchema) -> requests_Response:
        """
        Метод удаления балансировки.

        :param request: Словарь с logic_group (logicGroup).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}/api/balancing/',
                           json=request.model_dump(by_alias=True))


def get_balancing_session(access_token: str) -> BalancingSession:
    """
    Функция создаёт экземпляр BalancingSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию BalancingSession.
    """
    return BalancingSession(session=get_private_http_session(access_token=access_token))