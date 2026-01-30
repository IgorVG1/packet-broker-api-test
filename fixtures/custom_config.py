import pytest
from pydantic import BaseModel

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.custom_config.custom_config_client import CustomConfigClient, get_custom_config_client, \
    get_unauthorised_custom_config_client
from clients.custom_config.custom_config_schema import UploadCustomConfigRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from config import settings
from fixtures.authentication import UserFixture


class CustomConfigFixture(BaseModel):
    request: UploadCustomConfigRequestSchema


@pytest.fixture(scope='function')
def custom_config_client(function_user: UserFixture) -> CustomConfigClient:
    return get_custom_config_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_custom_config_client() -> CustomConfigClient:
    return get_unauthorised_custom_config_client()


@pytest.fixture(scope='function')
def function_custom_config(custom_config_client: CustomConfigClient) -> CustomConfigFixture:
    """
    Фикстура для загрузки на коммутатор валидной тестовой конфигурации.
    Тестовая конфигурацию: "testdata/files/test_conf.json"

    :param custom_config_client: Фикстура с подготовленным клиентом для работы с /api/custom_config/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на загрузку конфигурации.
    """
    request = UploadCustomConfigRequestSchema()
    custom_config_client.upload_custom_config_api(request=request)
    return CustomConfigFixture(request=request)


@pytest.fixture(scope='function')
def function_custom_config_tear_down(custom_config_client: CustomConfigClient):
    """
    Фикстура для загрузки на коммутатор валидной тестовой конфигурации.
    Тестовая конфигурацию: "testdata/files/test_conf.json"

    :param custom_config_client: Фикстура с подготовленным клиентом для работы с /api/custom_config/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на загрузку конфигурации.
    """
    yield
    request = UploadCustomConfigRequestSchema()
    custom_config_client.upload_custom_config_api(request=request)