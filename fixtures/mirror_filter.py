import pytest
from pydantic import BaseModel

from clients.custom_config.custom_config_client import CustomConfigClient
from clients.custom_config.custom_config_schema import UploadCustomConfigRequestSchema
from clients.mirror_filter.mirror_filter_client import MirrorFilterClient, get_mirror_filter_client, \
    get_unauthorized_mirror_filter_client, MirrorFilterSession, get_mirror_filter_session, \
    get_unauthorized_mirror_filter_session
from clients.mirror_filter.mirror_filter_schema import CreateMirrorFilterRequestSchema, DeleteMirrorFilterRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('MIRROR_FILTER_FIXTURE')


class MirrorFilterFixture(BaseModel):
    request: CreateMirrorFilterRequestSchema



@pytest.fixture(scope='function')
def mirror_filter_client(function_user: UserFixture) -> MirrorFilterClient:
    return get_mirror_filter_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorized_mirror_filter_client() -> MirrorFilterClient:
    return get_unauthorized_mirror_filter_client()

@pytest.fixture(scope='function')
def mirror_filter_session(function_user: UserFixture) -> MirrorFilterSession:
    return get_mirror_filter_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorized_mirror_filter_session() -> MirrorFilterSession:
    return get_unauthorized_mirror_filter_session()


@pytest.fixture(scope='function')
def function_mirror_filter_set_up(custom_config_client: CustomConfigClient):
    """
    Фикстура для загрузки тестовой конфигурации коммутатора перед началом теста.

    :param custom_config_client: Фикстура с подготовленным клиентом для работы с /api/custom_config/.
    """
    request = UploadCustomConfigRequestSchema()
    custom_config_client.upload_custom_config_api(request=request)

    logger.info('[Set-up completed] : Test custom config was uploaded.')


@pytest.fixture(scope='function')
def function_mirror_filter(mirror_filter_client: MirrorFilterClient) -> MirrorFilterFixture:
    """
    Фикстура для предварительного добавления правила фильтрации зеркалирования.

    :param mirror_filter_client: Фикстура с подготовленным клиентом для работы с /api/mirror_filter/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на добавление правила фильтрации зеркалирования.
    """
    request = CreateMirrorFilterRequestSchema()
    mirror_filter_client.create_mirror_filter_api(request=request)
    return MirrorFilterFixture(request=request)


@pytest.fixture(scope='function')
def function_mirror_filter_tear_down(mirror_filter_session: MirrorFilterSession):
    """
    Фикстура для удаления добавленного правила фильтрации зеркалирования по окончании теста.

    :param mirror_filter_session: Фикстура с подготовленным клиентом для работы с /api/mirror_filter/.
    """
    yield
    request = DeleteMirrorFilterRequestSchema()
    mirror_filter_session.delete_mirror_filters(request=request)

    logger.info('[Tear-down completed] : Created mirror filter was deleted.')