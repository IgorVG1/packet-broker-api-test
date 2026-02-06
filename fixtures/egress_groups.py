import pytest
from pydantic import BaseModel

from clients.custom_config.custom_config_client import CustomConfigClient
from clients.custom_config.custom_config_schema import UploadCustomConfigRequestSchema
from clients.egress_groups.egress_groups_client import EgressGroupsClient, get_egress_groups_client, \
    get_unauthorised_egress_groups_client, EgressGroupsSession, get_egress_groups_session, \
    get_unauthorised_egress_groups_session
from clients.egress_groups.egress_groups_schema import CreateEgressGroupRequestSchema, DeleteEgressGroupRequestSchema
from clients.ingress_groups.ingress_groups_client import IngressGroupsClient, IngressGroupsSession, \
    get_ingress_group_client, get_unauthorised_ingress_group_client, get_ingress_group_session, \
    get_unauthorised_ingress_group_session
from clients.ingress_groups.ingress_groups_schema import CreateIngressGroupRequestSchema, \
    DeleteIngressGroupRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('EGRESS_GROUPS_FIXTURE')


class EgressGroupFixture(BaseModel):
    request: CreateEgressGroupRequestSchema


@pytest.fixture(scope='function')
def egress_groups_client(function_user: UserFixture) -> EgressGroupsClient:
    return get_egress_groups_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_egress_groups_client() -> EgressGroupsClient:
    return get_unauthorised_egress_groups_client()


@pytest.fixture(scope='function')
def egress_groups_session(function_user: UserFixture) -> EgressGroupsSession:
    return get_egress_groups_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorised_egress_groups_session() -> EgressGroupsSession:
    return get_unauthorised_egress_groups_session()


@pytest.fixture(scope='function')
def function_egress_group(egress_groups_client: EgressGroupsClient) -> EgressGroupFixture:
    """
    Фикстура для предварительного создания входной группы.

    :param egress_groups_client: Фикстура с подготовленным клиентом для работы с /api/egress_groups/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на создание выходной группы.
    """
    request = CreateEgressGroupRequestSchema()
    egress_groups_client.create_egress_group_api(request=request)
    return EgressGroupFixture(request=request)


@pytest.fixture(scope='function')
def function_egress_group_tear_down(egress_groups_session: EgressGroupsSession):
    """
    Фикстура для удаления созданной выходной группы по окончании теста.

    :param egress_groups_session: Фикстура с подготовленной сессией для работы с /api/egress_groups/.
    """
    yield
    request = DeleteEgressGroupRequestSchema()
    egress_groups_session.delete_egress_group_api(request=request)

    logger.info('[Tear-down completed] : Created egress group was deleted.')


@pytest.fixture(scope='function')
def function_egress_group_return_config(custom_config_client: CustomConfigClient):
    """
    Фикстура для возврата тестовой конфигурации по окончании теста.

    :param custom_config_client: Фикстура с подготовленной сессией для работы с /api/custom_config/.
    """
    yield
    request = UploadCustomConfigRequestSchema()
    custom_config_client.upload_custom_config_api(request=request)

    logger.info('[Tear-down completed] : Test custom config was uploaded.')