import allure
from httpx import Response
from clients.api_client import APIClient
from clients.authentication_client.authentication_schema import LoginRequestSchema, LoginResponseSchema, \
    RefreshRequestSchema, RefreshResponseSchema
from clients.public_http_builder import get_public_http_client
from tools.routes import APIRoutes


class AuthenticationClient(APIClient):
    """
    Клиент для работы с /api/token/
    """
    @allure.step('Get access token used by username and password')
    def login_api(self, request: LoginRequestSchema) -> Response:
        """
        Метод выполняет аутентификацию пользователя.

        :param request: Словарь с username и password.
        :return: Ответ от сервера.
        """
        return self.post(url=f'{APIRoutes.AUTHENTICATION}/access/',
                         json=request.model_dump())

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        """
        Метод выполняет десериализацию ответа сервера на аутентификацию пользователя.

        :param request: Словарь с username и password.
        :return: LoginResponseSchema: pydantic-model ответа от сервера
        """
        response = self.login_api(request=request)
        return LoginResponseSchema.model_validate_json(response.text)

    @allure.step('Refresh access token used by refresh_token')
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """
        Метод выполняет обновление access_token.

        :param request: Словарь с refresh_token.
        :return: Ответ от сервера.
        """
        return self.post(url=f'{APIRoutes.AUTHENTICATION}/both/',
                         json=request.model_dump())

    def refresh(self, request: RefreshRequestSchema) -> RefreshResponseSchema:
        """
        Метод выполняет десериализацию ответа сервера на обновление access_token.

        :param request: Словарь с refresh_token.
        :return: RefreshResponseSchema: pydantic-model ответа от сервера
        """
        response = self.refresh_api(request=request)
        return RefreshResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    """
    Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AuthenticationClient.
    """
    return AuthenticationClient(client=get_public_http_client())