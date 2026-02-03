import pytest

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema
from clients.custom_config.custom_config_client import get_custom_config_client
from clients.private_http_builder import AuthenticationUserSchema
from tools.logger import get_logger

logger = get_logger(name='SESSION_TEAR-DOWN')


@pytest.fixture(scope='session', autouse=True)
def session_default_config():
    """
    Фикстура для загрузки на коммутатор конфигурации по умолчанию после прогоном всех тестов.
    Запускается один раз за прогон в самом конце после прохождения последнего теста.
    """
    yield
    authentication_client = get_authentication_client()
    authentication_request = LoginRequestSchema()
    authentication_client.login(request=authentication_request)

    user = AuthenticationUserSchema()

    custom_config_client = get_custom_config_client(user=user)
    custom_config_client.return_default_config()

    logger.info("Default config was returned on switch")