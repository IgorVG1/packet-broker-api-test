import pytest

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.custom_config.custom_config_client import get_custom_config_client
from clients.custom_config.custom_config_schema import UploadCustomConfigRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from tools.logger import get_logger

logger = get_logger(name='SESSION_SETUP')


@pytest.fixture(scope='session', autouse=True)
def session_custom_config():
    """
    Фикстура для загрузки на коммутатор валидной тестовой конфигурации перед прогоном всех тестов.
    Запускается один раз за прогон в самом начале перед запуском первого теста.
    Тестовая конфигурация: "testdata/files/test_conf.json"
    """
    authentication_client = get_authentication_client()
    authentication_request = LoginRequestSchema()
    authentication_client.login(request=authentication_request)

    user = AuthenticationUserSchema()

    custom_config_client = get_custom_config_client(user=user)
    custom_config_request = UploadCustomConfigRequestSchema()
    custom_config_client.upload_custom_config_api(request=custom_config_request)

    logger.info("Test custom config was uploaded on switch")