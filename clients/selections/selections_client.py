import allure
from httpx import Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from clients.selections.selections_schema import CreateSelectionRequestSchema, DeleteSelectionRequestSchema
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class SelectionsClient(APIClient):
    """
    Клиент для работы с /api/selections/
    """
    @allure.step('Get selections list')
    @tracker.track_coverage_httpx(f'{APIRoutes.SELECTIONS}')
    def get_selections_list_api(self) -> Response:
        """
        Метод получения списка групп отбора.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.SELECTIONS}')


    @allure.step('Create selection group')
    @tracker.track_coverage_httpx(f'{APIRoutes.SELECTIONS}')
    def create_selection_api(self, request: CreateSelectionRequestSchema) -> Response:
        """
        Метод создания группы отбора.

        :param request: Словарь CreateNodesRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.SELECTIONS}',
                         json=request.model_dump(by_alias=True))


def get_selections_client(user: AuthenticationUserSchema) -> SelectionsClient:
    """
    Функция создаёт экземпляр SelectionsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию SelectionsClient.
    """
    return SelectionsClient(client=get_private_http_client(user=user))


def get_unauthorised_selections_client() -> SelectionsClient:
    """
    Функция создаёт экземпляр неавторизованного SelectionsClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию SelectionsClient без авторизации.
    """
    return SelectionsClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class SelectionsSession(APISession):

    @allure.step('Delete selection group')
    @tracker.track_coverage_requests(f'{APIRoutes.SELECTIONS}')
    def delete_selection_api(self, request: DeleteSelectionRequestSchema) -> Response:
        """
        Метод удаления группы отбора.

        :param request: Словарь DeleteSelectionRequestSchema.model_dump(by_alias=True).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.SELECTIONS}',
                           json=request.model_dump(by_alias=True))


def get_selections_session(access_token: str) -> SelectionsSession:
    """
    Функция создаёт экземпляр SelectionsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию SelectionsSession.
    """
    return SelectionsSession(session=get_private_http_session(access_token=access_token))


def get_unauthorised_selections_session() -> SelectionsSession:
    """
    Функция создаёт экземпляр неавторизованного SelectionsSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию SelectionsSession без авторизации.
    """
    return SelectionsSession(session=get_public_http_session())