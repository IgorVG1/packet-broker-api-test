import allure
from httpx import Response

from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.custom_config.custom_config_schema import UploadCustomConfigRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.public_http_builder import get_public_http_client
from tools.routes import APIRoutes


class CustomConfigClient(APIClient):
    """
    Клиент для работы с /api/custom_config/ (/api/default_config/)
    """

    @allure.step('Download custom config')
    @tracker.track_coverage_httpx(f'{APIRoutes.CUSTOM_CONFIG}')
    def download_custom_config_api(self) -> Response:
        """
        Метод скачивания текущей конфигурации в формате JSON файла.
        "Скачать текущую конфигурацию"

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.CUSTOM_CONFIG}')


    @allure.step('Upload custom config')
    @tracker.track_coverage_httpx(f'{APIRoutes.CUSTOM_CONFIG}')
    def upload_custom_config_api(self, request: UploadCustomConfigRequestSchema) -> Response:
        """
        Метод загрузки на коммутатор пользовательского конфигурационного файла формате JSON.
        "Загрузить новую конфигурацию"

        :param request: Словарь с config (путь к файлу).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.CUSTOM_CONFIG}',
                         files={"config": request.config.read_bytes()})


    @allure.step('Saving custom config')
    @tracker.track_coverage_httpx(f'{APIRoutes.CUSTOM_CONFIG}')
    def saving_custom_config_api(self) -> Response:
        """
        Метод сохранения текущей конфигурации коммутатора.
        "Сохранить текущую конфигурацию"

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.put(url=f'{APIRoutes.CUSTOM_CONFIG}')


    @allure.step('Restore custom config')
    @tracker.track_coverage_httpx(f'{APIRoutes.CUSTOM_CONFIG}')
    def restore_custom_config_api(self) -> Response:
        """
        Метод применения сохраненной конфигурации.
        "Вернуть сохраненную конфигурацию"

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(url=f'{APIRoutes.CUSTOM_CONFIG}')


    @allure.step('Return default config')
    @tracker.track_coverage_httpx(f'{APIRoutes.DEFAULT_CONFIG}')
    def return_default_config(self) -> Response:
        """
        Метод применения конфигурации по умолчанию.
        "Вернуть конфигурацию по умолчанию"

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(url=f'{APIRoutes.DEFAULT_CONFIG}')




    @allure.step('Get switch info')
    @tracker.track_coverage_httpx(f'{APIRoutes.SWITCH_INFO}')
    def get_switch_info_api(self):
        """
        Метод получения системной информации коммутатора.

        :return: Ответ от сервера.
        """
        return self.get(url=f'{APIRoutes.SWITCH_INFO}')


def get_custom_config_client(user: AuthenticationUserSchema) -> CustomConfigClient:
    """
    Функция создаёт экземпляр CustomConfigClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CustomConfigClient.
    """
    return CustomConfigClient(client=get_private_http_client(user=user))


def get_unauthorised_custom_config_client() -> CustomConfigClient:
    """
    Функция создаёт экземпляр неавторизованного CustomConfigClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CustomConfigClient без авторизации.
    """
    return CustomConfigClient(client=get_public_http_client())