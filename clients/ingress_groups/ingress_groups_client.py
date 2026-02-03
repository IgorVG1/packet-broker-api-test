import allure
from httpx import Response
from requests import Response as requests_Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.ingress_groups.ingress_groups_schema import CreateIngressGroupRequestSchema, \
    UpdateIngressGroupRequestSchema, DeleteIngressGroupRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class IngressGroupsClient(APIClient):
    """
    Клиент для работы с /api/ingress_groups/
    """
    @allure.step('Get ingress group list')
    @tracker.track_coverage_httpx(f'{APIRoutes.INGRESS_GROUPS}')
    def get_ingress_group_list_api(self) -> Response:
        """
        Метод вывода списка входных групп.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.INGRESS_GROUPS}')


    @allure.step('Create ingress group')
    @tracker.track_coverage_httpx(f'{APIRoutes.INGRESS_GROUPS}')
    def create_ingress_group_api(self, request: CreateIngressGroupRequestSchema) -> Response:
        """
        Метод создания входной группы.

        :param request: Словарь CreateIngressGroupRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.INGRESS_GROUPS}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Update ingress group')
    @tracker.track_coverage_httpx(f'{APIRoutes.INGRESS_GROUPS}')
    def update_ingress_group_api(self, request: UpdateIngressGroupRequestSchema) -> Response:
        """
        Метод изменения входной группы.

        :param request: Словарь UpdateIngressGroupRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.INGRESS_GROUPS}',
                        json=request.model_dump(by_alias=True))


def get_ingress_group_client(user: AuthenticationUserSchema) -> IngressGroupsClient:
    """
    Функция создаёт экземпляр IngressGroupsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию IngressGroupsClient.
    """
    return IngressGroupsClient(client=get_private_http_client(user=user))


def get_unauthorised_ingress_group_client() -> IngressGroupsClient:
    """
    Функция создаёт экземпляр неавторизованного IngressGroupsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию IngressGroupsClient без авторизации.
    """
    return IngressGroupsClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class IngressGroupsSession(APISession):

    @allure.step('Delete ingress group')
    @tracker.track_coverage_requests(f'{APIRoutes.INGRESS_GROUPS}')
    def delete_ingress_group_api(self, request: DeleteIngressGroupRequestSchema) -> requests_Response:
        """
        Метод удаления входной группы.

        :param request: Словарь DeleteIngressGroupRequestSchema.model_dump(by_alias=True).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.INGRESS_GROUPS}',
                           json=request.model_dump(by_alias=True))


    @allure.step('Delete nonexistent ingress group')
    @tracker.track_coverage_requests(f'{APIRoutes.PORTS}')
    def incorrect_delete_ingress_group_api(self) -> requests_Response:
        """
        Метод для обработки ошибки [412] с помощью удаления не существующей входной группы.

        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.INGRESS_GROUPS}')


def get_ingress_group_session(access_token: str) -> IngressGroupsSession:
    """
    Функция создаёт экземпляр IngressGroupsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию IngressGroupsSession.
    """
    return IngressGroupsSession(session=get_private_http_session(access_token=access_token))


def get_unauthorised_ingress_group_session() -> IngressGroupsSession:
    """
    Функция создаёт экземпляр неавторизованного IngressGroupsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию IngressGroupsSession без авторизации.
    """
    return IngressGroupsSession(session=get_public_http_session())