import pytest
from pydantic import BaseModel

from clients.ingress_groups.ingress_groups_client import IngressGroupsClient, IngressGroupsSession, \
    get_ingress_group_client, get_unauthorised_ingress_group_client, get_ingress_group_session, \
    get_unauthorised_ingress_group_session
from clients.ingress_groups.ingress_groups_schema import CreateIngressGroupRequestSchema, \
    DeleteIngressGroupRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('INGRESS_GROUPS_FIXTURE')


class IngressGroupFixture(BaseModel):
    request: CreateIngressGroupRequestSchema


@pytest.fixture(scope='function')
def ingress_groups_client(function_user: UserFixture) -> IngressGroupsClient:
    return get_ingress_group_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_ingress_groups_client(function_user: UserFixture) -> IngressGroupsClient:
    return get_unauthorised_ingress_group_client()


@pytest.fixture(scope='function')
def ingress_groups_session(function_user: UserFixture) -> IngressGroupsSession:
    return get_ingress_group_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorised_ingress_groups_session(function_user: UserFixture) -> IngressGroupsSession:
    return get_unauthorised_ingress_group_session()


@pytest.fixture(scope='function')
def function_ingress_groups(ingress_groups_client: IngressGroupsClient) -> IngressGroupFixture:
    """
    Фикстура для предварительного создания входной группы.

    :param ingress_groups_client: Фикстура с подготовленным клиентом для работы с /api/ingress_groups/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на создание сконфигурированного порта.
    """
    request = CreateIngressGroupRequestSchema()
    ingress_groups_client.create_ingress_group_api(request=request)
    return IngressGroupFixture(request=request)


@pytest.fixture(scope='function')
def function_ingress_groups_set_up(ingress_groups_session: IngressGroupsSession):
    """
    Фикстура для удаления существующей входной группы перед запуском теста.

    :param ingress_groups_session: Фикстура с подготовленной сессией для работы с /api/ingress_groups/.
    """
    try:
        request = DeleteIngressGroupRequestSchema()
        ingress_groups_session.delete_ingress_group_api(request=request)
        ingress_groups_session.delete_ingress_group_api(request=request)
    finally:
        logger.info('[Set-up completed] : Existed ingress group was deleted.')


@pytest.fixture(scope='function')
def function_ingress_groups_tear_down(ingress_groups_session: IngressGroupsSession):
    """
    Фикстура для удаления созданной входной группы по окончании теста.

    :param ingress_groups_session: Фикстура с подготовленной сессией для работы с /api/ingress_groups/.
    """
    yield
    request = DeleteIngressGroupRequestSchema()
    ingress_groups_session.delete_ingress_group_api(request=request)

    logger.info('[Tear-down completed] : Created ingress group was deleted.')