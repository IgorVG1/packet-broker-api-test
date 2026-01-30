import allure
from typing import List, Any
from httpx import Response
from pydantic import BaseModel
from requests import Response as requests_Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.filters.filters_schema import CreateFiltersRequestSchema, DeleteFiltersRequestSchema, CreateFilterSchema, \
    DeleteFilterSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes


class FiltersClient(APIClient):
    """
    Клиент для работы с /api/filters/
    """

    def get_filters_api(self) -> Response:
        """
        Метод получения списка сконфигурированных фильтров.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.FILTERS}')


    def create_filters_api(self, request: CreateFilterSchema) -> Response:
        """
        Метод добавления фильтров.
        "Настройки правил фильтрации" на странице http://192.168.7.57/configuration/.

        :param request: Список словарей на основе модели CreateFilterSchema.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.FILTERS}',
                         json=[request.model_dump(by_alias=True)])


def get_filters_client(user: AuthenticationUserSchema) -> FiltersClient:
    """
    Функция создаёт экземпляр FiltersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию FiltersClient.
    """
    return FiltersClient(client=get_private_http_client(user=user))


def get_unauthorised_filters_client() -> FiltersClient:
    """
    Функция создаёт экземпляр неавторизованного FiltersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию FiltersClient без авторизации.
    """
    return FiltersClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class FiltersSession(APISession):

    @allure.step('Delete filters group')
    @tracker.track_coverage_requests(f'{APIRoutes.FILTERS}')
    def delete_filters_api(self, request: DeleteFiltersRequestSchema) -> requests_Response:
        """
        Метод удаления фильтров.

        :param request: Список словарей на основе модели DeleteFilterSchema.
        :return: Объект requests.Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.FILTERS}',
                           json=request)


def get_filters_session(access_token: str) -> FiltersSession:
    """
    Функция создаёт экземпляр FiltersSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию FiltersSession.
    """
    return FiltersSession(session=get_private_http_session(access_token=access_token))


def get_unauthorised_filters_session() -> FiltersSession:
    """
    Функция создаёт экземпляр неавторизованного FiltersSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию FiltersSession без авторизации.
    """
    return FiltersSession(session=get_public_http_session())