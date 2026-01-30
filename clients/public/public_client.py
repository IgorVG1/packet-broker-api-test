import allure
from httpx import Response
from requests import Response as requests_Response

from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    UpdateAdditionalFiltersRequestSchema, DeleteAdditionalFiltersRequestSchema
from clients.api_client import APIClient
from clients.api_session import APISession
from clients.balancing.balancing_schema import CreateBalancingRequestSchema, UpdateBalancingRequestSchema, \
    DeleteBalancingRequestSchema
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes
from clients.api_coverage import tracker


class PublicClient(APIClient):
    """
    Клиент для работы без access_token (валидация ошибки [403]FORBIDDEN)
    """
#-----------------------------------------------------------------------------------------------------------------------
    @allure.step('Create additional filters')
    @tracker.track_coverage_httpx(f'{APIRoutes.ADDITIONAL_FILTERS}')
    def create_additional_filters_api(self, request: CreateAdditionalFiltersRequestSchema) -> Response:
        """
        Метод создает дополнительные фильтры.

        :param request: Список словарей с direction, group_id(groupId), ip, type.
        :return: Ответ от сервера.
        """
        json_data = request.model_dump(by_alias=True)
        return self.post(url=f'{APIRoutes.ADDITIONAL_FILTERS}',
                         json=json_data)


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



# ----------------------------------------------------------------------------------------------------------------------



    @allure.step('Get balancing list')
    @tracker.track_coverage_httpx(f'{APIRoutes.BALANCING}')
    def get_balancing_list_api(self) -> Response:
        """
        Метод получения списка сконфигурированных групп балансировки.

        :param request: Словарь с logic_id(logicId), balance_type(balanceType).
        :return: Ответ от сервера.
        """
        return self.get(url=f'{APIRoutes.BALANCING}')


    @allure.step('Create balancing(s) group(s)')
    @tracker.track_coverage_httpx(f'{APIRoutes.BALANCING}')
    def create_balancing_api(self, request: CreateBalancingRequestSchema) -> Response:
        """
        Метод создает балансировку(и) групп(ы).

        :param request: Список словарей с logic_id(logicId), balance_type(balanceType).
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



#======================================================================================================================



class PublicSession(APISession):
    """
    Сессия для работы без access_token (валидация ошибки [403]FORBIDDEN)
    """
    @allure.step('Delete additional filters')
    @tracker.track_coverage_requests(f'{APIRoutes.ADDITIONAL_FILTERS}')
    def delete_additional_filters_api(self, request: DeleteAdditionalFiltersRequestSchema) -> requests_Response:
        """
        Метод удаления дополнительных фильтров.

        :param request: Список словарей с value: str, direction: str, logic_group (logicGroup): int, type: str.
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}/api/additional_filters/',
                           json=request.model_dump())

#-----------------------------------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------------------------------



#=======================================================================================================================



def get_public_client() -> PublicClient:
    """
    Функция создаёт экземпляр PublicClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PublicClient.
    """
    return PublicClient(client=get_public_http_client())


def get_public_session() -> PublicSession:
    """
    Функция создаёт экземпляр PublicSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PublicSession.
    """
    return PublicSession(session=get_public_http_session())