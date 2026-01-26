import pytest
from pydantic import BaseModel
from clients.balancing.balancing_client import BalancingClient, get_balancing_client, BalancingSession, \
    get_balancing_session
from clients.balancing.balancing_schema import CreateBalancingRequestSchema
from fixtures.authentication import UserFixture


class BalancingFixture(BaseModel):
    request: CreateBalancingRequestSchema


@pytest.fixture(scope='function')
def balancing_client(function_user: UserFixture) -> BalancingClient:
    return get_balancing_client(user=function_user.authentication_user)


@pytest.fixture(scope='function')
def balancing_session(function_user: UserFixture) -> BalancingSession:
    return get_balancing_session(access_token=function_user.access_token)


@pytest.fixture(scope='function')
def function_balancing(balancing_client: BalancingClient) -> BalancingFixture:
    request_create = CreateBalancingRequestSchema()
    balancing_client.create_balancing_api(request=request_create)
    return BalancingFixture(request=request_create)


@pytest.fixture(scope='function')
def function_balancing_after_delete(balancing_client: BalancingClient):
    yield
    request_create = CreateBalancingRequestSchema()
    balancing_client.create_balancing_api(request=request_create)