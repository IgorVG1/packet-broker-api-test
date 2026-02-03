import pytest
from pydantic import BaseModel
from clients.loopback_ports.loopback_ports_client import LoopbackPortsClient, get_loopback_ports_client, LoopbackPortsSession, \
    get_loopback_ports_session, get_unauthorised_loopback_ports_client, get_unauthorised_loopback_ports_session
from clients.loopback_ports.loopback_ports_schema import CreateLoopbackPortsRequestSchema, DeleteLoopbackPortsRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('LOOPBACK_PORTS_FIXTURE')


class LoopbackPortsFixture(BaseModel):
    request: CreateLoopbackPortsRequestSchema


@pytest.fixture(scope='function')
def loopback_ports_client(function_user: UserFixture) -> LoopbackPortsClient:
    return get_loopback_ports_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_loopback_ports_client() -> LoopbackPortsClient:
    return get_unauthorised_loopback_ports_client()


@pytest.fixture(scope='function')
def loopback_ports_session(function_user: UserFixture) -> LoopbackPortsSession:
    return get_loopback_ports_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorised_loopback_ports_session() -> LoopbackPortsSession:
    return get_unauthorised_loopback_ports_session()


@pytest.fixture(scope='function')
def function_loopback_port(loopback_ports_client: LoopbackPortsClient) -> LoopbackPortsFixture:
    request = CreateLoopbackPortsRequestSchema()
    loopback_ports_client.create_loopback_ports(request=request)

    logger.info('[Set-up completed] : Loopback port was created.')

    return LoopbackPortsFixture(request=request)


@pytest.fixture(scope='function')
def function_loopback_port_set_up(loopback_ports_session: LoopbackPortsSession):
    try:
        request = DeleteLoopbackPortsRequestSchema()
        loopback_ports_session.delete_loopback_ports(request=request)
    finally:
        logger.info('[Tear-down completed] : If speed limits for actual loopback ports existed - now they were deleted.')


@pytest.fixture(scope='function')
def function_loopback_port_tear_down(loopback_ports_session: LoopbackPortsSession):
    yield
    request = DeleteLoopbackPortsRequestSchema()
    loopback_ports_session.delete_loopback_ports(request=request)

    logger.info('[Tear-down completed] : Changed loopback port was deleted.')