import allure
from httpx import Response
from requests import Response as requests_Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.mirror_filter.mirror_filter_schema import CreateMirrorFilterRequestSchema, DeleteMirrorFilterRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class MirrorFilterClient(APIClient):
    """
    Клиент для работы с /api/mirror_filter/ и /api/psf_mirror_filter/.
    """

    @allure.step('Get mirror filter list')
    @tracker.track_coverage_httpx(f'{APIRoutes.MIRROR_FILTER}')
    def get_mirror_filter_list(self) -> Response:
        """
        Метод получения списка правил фильтрации зеркалирования.
        При загрузке страницы http://192.168.7.57/psf_format/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.MIRROR_FILTER}')


    @allure.step('Create mirror filter')
    @tracker.track_coverage_httpx(f'{APIRoutes.MIRROR_FILTER}')
    def create_mirror_filter_api(self, request: CreateMirrorFilterRequestSchema) -> Response:
        """
        Метод получения списка правил фильтрации зеркалирования.
        При загрузке страницы http://192.168.7.57/psf_format/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.MIRROR_FILTER}',
                         json=request.model_dump(by_alias=True))




    @allure.step('Get PSF mirror filter list')
    @tracker.track_coverage_httpx(f'{APIRoutes.PSF_MIRROR_FILTER}')
    def get_psf_mirror_filter_list_api(self) -> Response:
        """
        Метод получения правил фильтрации зеркалирования PSF.
        При загрузке страницы http://192.168.7.57/psf_format/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.PSF_MIRROR_FILTER}')




def get_mirror_filter_client(user: AuthenticationUserSchema) -> MirrorFilterClient:
    """
    Функция создаёт экземпляр MirrorFilterClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirrorFilterClient.
    """
    return MirrorFilterClient(client=get_private_http_client(user=user))

def get_unauthorized_mirror_filter_client() -> MirrorFilterClient:
    """
    Функция создаёт экземпляр неавторизованного MirrorFilterClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirrorFilterClient без авторизации.
    """
    return MirrorFilterClient(client=get_public_http_client())

#-----------------------------------------------------------------------------------------------------------------------

class MirrorFilterSession(APISession):

    @allure.step('Delete mirror filters')
    @tracker.track_coverage_requests(f'{APIRoutes.MIRROR_FILTER}')
    def delete_mirror_filters(self, request: DeleteMirrorFilterRequestSchema) -> requests_Response:

        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.MIRROR_FILTER}',
                           json=request.model_dump(by_alias=True))


def get_mirror_filter_session(access_token: str) -> MirrorFilterSession:
    """
    Функция создаёт экземпляр MirrorFilterSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirrorFilterSession.
    """
    return MirrorFilterSession(get_private_http_session(access_token=access_token))

def get_unauthorized_mirror_filter_session() -> MirrorFilterSession:
    """
    Функция создаёт экземпляр неавторизованного MirrorFilterSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию MirrorFilterSession без авторизации.
    """
    return MirrorFilterSession(get_public_http_session())