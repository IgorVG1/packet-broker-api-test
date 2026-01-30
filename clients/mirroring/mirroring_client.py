import allure
from httpx import Response
from requests import Response as requests_Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.mirroring.mirroring_schema import CreateMirroringRequestSchema, UpdateMirroringRequestSchema, \
    DeleteMirroringRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class MirroringClient(APIClient):
    """
    Клиент для работы с /api/mirroring/
    """
    @allure.step('Get mirroring list')
    @tracker.track_coverage_httpx(f'{APIRoutes.MIRRORING}')
    def get_mirroring_list_api(self) -> Response:
        """
        Метод вывода списка групп зеркалирования.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.MIRRORING}')


    @allure.step('Create mirroring group')
    @tracker.track_coverage_httpx(f'{APIRoutes.MIRRORING}')
    def create_mirroring_api(self, request: CreateMirroringRequestSchema) -> Response:
        """
        Метод создания группы зеркалирования.

        :param request: Словарь CreateMirroringRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.MIRRORING}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Update mirroring group')
    @tracker.track_coverage_httpx(f'{APIRoutes.MIRRORING}')
    def update_mirroring_api(self, request: UpdateMirroringRequestSchema) -> Response:
        """
        Метод изменения группы зеркалирования.

        :param request: Словарь UpdateMirroringRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.MIRRORING}',
                        json=request.model_dump(by_alias=True))


def get_mirroring_client(user: AuthenticationUserSchema) -> MirroringClient:
    """
    Функция создаёт экземпляр MirroringClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirroringClient.
    """
    return MirroringClient(client=get_private_http_client(user=user))


def get_unauthorised_mirroring_client() -> MirroringClient:
    """
    Функция создаёт экземпляр неавторизованного MirroringClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirroringClient без авторизации.
    """
    return MirroringClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class MirroringSession(APISession):

    @allure.step('Delete mirroring group')
    @tracker.track_coverage_requests(f'{APIRoutes.MIRRORING}')
    def delete_mirroring_api(self, request: DeleteMirroringRequestSchema) -> requests_Response:
        """
        Метод удаления балансировки.

        :param request: Словарь DeleteMirroringRequestSchema.model_dump(by_alias=True).
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.MIRRORING}',
                           json=request.model_dump(by_alias=True))


def get_mirroring_session(access_token: str) -> MirroringSession:
    """
    Функция создаёт экземпляр MirroringSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirroringSession.
    """
    return MirroringSession(session=get_private_http_session(access_token=access_token))


def get_unauthorised_mirroring_session() -> MirroringSession:
    """
    Функция создаёт экземпляр неавторизованного MirroringSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirroringSession без авторизации.
    """
    return MirroringSession(session=get_public_http_session())