import pytest

from clients.additional_filters.additional_filters_client import AdditionalFiltersClient, get_additional_filters_client
from fixtures.authentication import UserFixture


@pytest.fixture(scope='function')
def additional_filters_client(function_user: UserFixture) -> AdditionalFiltersClient:
    return get_additional_filters_client(user=function_user.authentication_user)