import allure
from httpx import Response
from requests import Response as requests_Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.api_session import APISession
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema, get_private_http_session
from clients.psf_format.psf_format_schema import CreatePsfFormatRequestSchema, UpdatePsfFormatRequestSchema, \
    DeletePsfFormatRequestSchema, CreatePsfDmacRequestSchema
from clients.public_http_builder import get_public_http_client, get_public_http_session
from config import settings
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class PsfFormatClient(APIClient):
    """
    Клиент для работы с /api/psf_format/ и /api/psf_dmac/.
    """

    @allure.step('Get psf format list')
    @tracker.track_coverage_httpx(f'{APIRoutes.PSF_FORMAT}')
    def get_psf_format_list_api(self) -> Response:
        """
        Метод получения списка правил спецформата.
        При загрузке страницы http://192.168.7.57/psf_format/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.PSF_FORMAT}')


    @allure.step('Create psf format')
    @tracker.track_coverage_httpx(f'{APIRoutes.PSF_FORMAT}')
    def create_psf_format_api(self, request: CreatePsfFormatRequestSchema) -> Response:
        """
        Метод добавления правила спецформата.

        :param request: Словарь CreatePsfFormatRequestSchema.model_dump().
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.PSF_FORMAT}',
                         json=request.model_dump())


    @allure.step('Update psf format')
    @tracker.track_coverage_httpx(f'{APIRoutes.PSF_FORMAT}')
    def update_psf_format_api(self, request: UpdatePsfFormatRequestSchema) -> Response:
        """
        Метод изменения правила спецформата.

        :param request: Словарь UpdatePsfFormatRequestSchema.model_dump().
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.PSF_FORMAT}',
                        json=request.model_dump())




    @allure.step('Get psf dmac')
    @tracker.track_coverage_httpx(f'{APIRoutes.PSF_DMAC}')
    def get_psf_dmac_api(self) -> Response:
        """
        Метод получения dMAC для формата PSF.
        При загрузке страницы http://192.168.7.57/psf_format/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.PSF_DMAC}')


    @allure.step('Create psf dmac')
    @tracker.track_coverage_httpx(f'{APIRoutes.PSF_DMAC}')
    def create_psf_dmac_api(self, request: CreatePsfDmacRequestSchema) -> Response:
        """
        Метод конфигурирования dMAC для формата PSF.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.PSF_DMAC}',
                         json=request.model_dump())




def get_psf_format_client(user: AuthenticationUserSchema) -> PsfFormatClient:
    """
    Функция создаёт экземпляр PsfFormatClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PsfFormatClient.
    """
    return PsfFormatClient(client=get_private_http_client(user=user))


def get_unauthorized_psf_format_client() -> PsfFormatClient:
    """
    Функция создаёт экземпляр неавторизованного PsfFormatClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PsfFormatClient без авторизации.
    """
    return PsfFormatClient(client=get_public_http_client())

# ----------------------------------------------------------------------------------------------------------------------

class PsfFormatSession(APISession):

    @allure.step('Delete psf format')
    @tracker.track_coverage_requests(f'{APIRoutes.PSF_FORMAT}')
    def delete_psf_format_api(self, request: DeletePsfFormatRequestSchema) -> requests_Response:
        """
        Метод удаления правила спецформата.

        :param request: Словарь DeletePsfFormatRequestSchema.model_dump().
        :return: Объект requests_Response с данными ответа.
        """
        return self.delete(url=f'{settings.http_client.client_url}{APIRoutes.PSF_FORMAT}',
                           json=request.model_dump())


def get_psf_format_session(access_token: str) -> PsfFormatSession:
    """
    Функция создаёт экземпляр PsfFormatSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PsfFormatSession.
    """
    return PsfFormatSession(session=get_private_http_session(access_token=access_token))


def get_unauthorized_psf_format_session() -> PsfFormatSession:
    """
    Функция создаёт экземпляр неавторизованного PsfFormatSession с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию PsfFormatSession без авторизации.
    """
    return PsfFormatSession(session=get_public_http_session())