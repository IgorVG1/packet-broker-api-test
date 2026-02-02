import pytest
from pydantic import BaseModel

from clients.ports.ports_client import PortsClient, get_ports_client, PortsSession, get_ports_session, \
    get_unauthorised_ports_client, get_unauthorised_ports_session
from clients.ports.ports_schema import CreatePortRequestSchema, DeletePortsRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('PORTS_FIXTURE')


class PortsFixture(BaseModel):
    request: CreatePortRequestSchema


@pytest.fixture(scope='function')
def ports_client(function_user: UserFixture) -> PortsClient:
    return get_ports_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_ports_client(function_user: UserFixture) -> PortsClient:
    return get_unauthorised_ports_client()


@pytest.fixture(scope='function')
def ports_session(function_user: UserFixture) -> PortsSession:
    return get_ports_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorised_ports_session(function_user: UserFixture) -> PortsSession:
    return get_unauthorised_ports_session()


@pytest.fixture(scope='function')
def function_ports(ports_client: PortsClient) -> PortsFixture:
    """
    Фикстура для предварительного создания сконфигурированного порта.

    :param ports_client: Фикстура с подготовленным клиентом для работы с /api/ports/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на создание сконфигурированного порта.
    """
    request = CreatePortRequestSchema()
    ports_client.create_ports_api(request=request)
    return PortsFixture(request=request)


@pytest.fixture(scope='function')
def function_ports_tear_down(ports_session: PortsSession):
    """
    Фикстура для удаления созданных фильтров по окончании теста.

    :param ports_session: Фикстура с подготовленной сессией для работы с /api/ports/.
    """
    yield
    request = DeletePortsRequestSchema()
    ports_session.delete_ports_api(request=request)

    logger.info('[Tear-down completed] : Created port was deleted.')