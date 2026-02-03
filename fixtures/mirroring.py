import pytest
from pydantic import BaseModel
from clients.mirroring.mirroring_client import MirroringClient, get_mirroring_client, get_unauthorised_mirroring_client, \
    MirroringSession, get_mirroring_session, get_unauthorised_mirroring_session
from clients.mirroring.mirroring_schema import CreateMirroringRequestSchema, DeleteMirroringRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('MIRRORING_FIXTURE')


class MirroringFixture(BaseModel):
    request: CreateMirroringRequestSchema


@pytest.fixture(scope='function')
def mirroring_client(function_user: UserFixture) -> MirroringClient:
    return get_mirroring_client(user=function_user.authentication_user)


@pytest.fixture(scope='function')
def unauthorised_mirroring_client() -> MirroringClient:
    return get_unauthorised_mirroring_client()


@pytest.fixture(scope='function')
def mirroring_session(function_user: UserFixture) -> MirroringSession:
    return get_mirroring_session(access_token=function_user.access_token)


@pytest.fixture(scope='function')
def unauthorised_mirroring_session() -> MirroringSession:
    return get_unauthorised_mirroring_session()


@pytest.fixture(scope='function')
def function_mirroring(mirroring_client: MirroringClient) -> MirroringFixture:
    """
    Фикстура для предварительного создания группы зеркалирования.

    :param mirroring_client: Фикстура с подготовленным клиентом для работы с /api/mirroring/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на создание группы зеркалирования.
    """
    request = CreateMirroringRequestSchema()
    mirroring_client.create_mirroring_api(request=request)
    return MirroringFixture(request=request)


@pytest.fixture(scope='function')
def function_mirroring_tear_down(mirroring_session: MirroringSession):
    """
    Фикстура для удаления созданной группы зеркалирования по окончании теста.

    :param mirroring_session: Фикстура с подготовленной сессией для работы с /api/mirroring/.
    """
    yield
    request = DeleteMirroringRequestSchema()
    mirroring_session.delete_mirroring_api(request=request)

    logger.info('[Tear-down completed] : Created mirroring group was deleted.')


@pytest.fixture(scope='function')
def function_mirroring_set_up(mirroring_session: MirroringSession):
    """
    Фикстура для удаления созданной группы зеркалирования перед запуском теста.

    :param mirroring_session: Фикстура с подготовленной сессией для работы с /api/mirroring/.
    """
    try:
        request = DeleteMirroringRequestSchema()
        mirroring_session.delete_mirroring_api(request=request)
    finally:
        logger.info('[Tear-down completed] : Created mirroring group was deleted.')
    yield