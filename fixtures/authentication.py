import pytest
from pydantic import BaseModel

from clients.authentication_client.authentication_client import AuthenticationClient, get_authentication_client
from clients.authentication_client.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.private_http_builder import AuthenticationUserSchema


class UserFixture(BaseModel):
    request: LoginRequestSchema
    response: LoginResponseSchema


    @property
    def username(self) -> str:
        return self.request.username

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def access_token(self) -> str:
        return self.response.access

    @property
    def refresh_token(self) -> str:
        return self.response.refresh

    @property
    def user_id(self) -> int:
        return self.response.user.id

    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        return AuthenticationUserSchema(username=self.username,
                                        password=self.password)


@pytest.fixture(scope='function')
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()


@pytest.fixture(scope='function')
def function_user(authentication_client: AuthenticationClient) -> UserFixture:
    request = LoginRequestSchema()
    response = authentication_client.login(request=request)
    return UserFixture(request=request,
                       response=response)