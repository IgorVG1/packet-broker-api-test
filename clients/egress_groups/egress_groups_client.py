import allure
from httpx import Response
from requests import Response as requests_Response
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

class EgressGroupsClient(APIClient):
    """
    Клиент для работы с /api/egress_groups/
    """

    @allure.step('Get egress group list')
    @tracker.track_coverage_httpx(f'{APIRoutes.EGRESS_GROUPS}')
    def get_egress_group_list_api(self) -> Response:
        """
        Метод вывода списка выходных групп.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.EGRESS_GROUPS}')


    @allure.step('Create egress group')
    @tracker.track_coverage_httpx(f'{APIRoutes.EGRESS_GROUPS}')
    def create_egress_group_api(self, request: CreateEgressGroupRequestSchema) -> Response:
        """
        Метод создания выходной группы.

        :param request: Словарь CreateEgressGroupRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.EGRESS_GROUPS}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Update egress group')
    @tracker.track_coverage_httpx(f'{APIRoutes.EGRESS_GROUPS}')
    def update_egress_group_api(self, request: UpdateEgressGroupRequestSchema) -> Response:
        """
        Метод обновления выходной группы.

        :param request: Словарь UpdateEgressGroupRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.EGRESS_GROUPS}',
                        json=request.model_dump(by_alias=True))


def get_egress_groups_client(user: AuthenticationUserSchema) -> EgressGroupsClient:
    """
    Функция создаёт экземпляр EgressGroupsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию EgressGroupsClient.
    """
    return EgressGroupsClient(client=get_private_http_client(user=user))

def get_unauthorised_egress_groups_client() -> EgressGroupsClient:
    """
    Функция создаёт экземпляр неавторизованного EgressGroupsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию EgressGroupsClient без авторизации.
    """
    return EgressGroupsClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class EgressGroupsSession(APISession):

    @allure.step('Delete egress group')
    @tracker.track_coverage_requests(f'{APIRoutes.EGRESS_GROUPS}')
    def delete_egress_group_api(self, request: DeleteEgressGroupRequestSchema) -> requests_Response:
        """
        Метод удаления выходной группы.

        :param request: Словарь DeleteEgressGroupRequestSchema.model_dump(by_alias=True).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.EGRESS_GROUPS}',
                           json=request.model_dump(by_alias=True))


def get_egress_groups_session(access_token: str) -> EgressGroupsSession:
    """
    Функция создаёт экземпляр EgressGroupsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию EgressGroupsSession.
    """
    return EgressGroupsSession(session=get_private_http_session(access_token=access_token))

def get_unauthorised_egress_groups_session() -> EgressGroupsSession:
    """
    Функция создаёт экземпляр неавторизованного EgressGroupsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию EgressGroupsSession без авторизации.
    """
    return EgressGroupsSession(session=get_public_http_session())