import allure
from httpx import Response
from requests import Response as requests_Response
from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    UpdateAdditionalFiltersRequestSchema, DeleteAdditionalFiltersRequestSchema
from clients.api_client import APIClient
from clients.api_session import APISession
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client, get_private_http_session
from config import settings
from tools.routes import APIRoutes
from clients.api_coverage import tracker

# ----------------------------------------------------------------------------------------------------------------------

class AdditionalFiltersClient(APIClient):
    """
    Клиент для работы с /api/additional_filters/
    """
    @allure.step('Create additional filters')
    @tracker.track_coverage_httpx(f'{APIRoutes.ADDITIONAL_FILTERS}')
    def create_additional_filters_api(self, request: CreateAdditionalFiltersRequestSchema) -> Response:
        """
        Метод создает дополнительные фильтры.

        :param request: Список словарей с direction, group_id(groupId), ip, type.
        :return: Ответ от сервера.
        """
        return self.post(url=f'{APIRoutes.ADDITIONAL_FILTERS}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Update additional filters')
    @tracker.track_coverage_httpx(f'{APIRoutes.ADDITIONAL_FILTERS}')
    def update_additional_filters_api(self, request: UpdateAdditionalFiltersRequestSchema) -> Response:
        """
        Метод сохраняет дополнительный фильтр.

        :param request: Список словарей с logic_id(logicId), filter_ip_white_enable(filterIPWhiteEnable), filter_ip_black_enable(filterIPBlackEnable).
        :return: Ответ от сервера.
        """
        return self.put(url=f'{APIRoutes.ADDITIONAL_FILTERS}',
                        json=request.model_dump(by_alias=True))


def get_additional_filters_client(user: AuthenticationUserSchema) -> AdditionalFiltersClient:
    """
    Функция создаёт экземпляр AdditionalFiltersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AdditionalFiltersClient.
    """
    return AdditionalFiltersClient(client=get_private_http_client(user=user))

# ----------------------------------------------------------------------------------------------------------------------

class AdditionalFiltersSession(APISession):

    @allure.step('Delete additional filters')
    @tracker.track_coverage_requests(f'{APIRoutes.ADDITIONAL_FILTERS}')
    def delete_additional_filters_api(self, request: DeleteAdditionalFiltersRequestSchema) -> requests_Response:
        """
        Метод удаления дополнительных фильтров.

        :param request: Список словарей с value: str, direction: str, logic_group (logicGroup): int, type: str.
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}/api/additional_filters/',
                           json=request.model_dump(by_alias=True))


def get_additional_filters_session(access_token: str) -> AdditionalFiltersSession:
    """
    Функция создаёт экземпляр AdditionalFiltersSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AdditionalFiltersSession.
    """
    return AdditionalFiltersSession(session=get_private_http_session(access_token=access_token))