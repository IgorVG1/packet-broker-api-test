import pytest
from pydantic import BaseModel
from clients.additional_filters.additional_filters_client import AdditionalFiltersClient, get_additional_filters_client
from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    CreateAdditionalFiltersSchema, CreateAdditionalFiltersResponseSchema
from fixtures.authentication import UserFixture


class AdditionalFilterFixture(BaseModel):
    request: CreateAdditionalFiltersRequestSchema


@pytest.fixture(scope='function')
def additional_filters_client(function_user: UserFixture) -> AdditionalFiltersClient:
    return get_additional_filters_client(user=function_user.authentication_user)


@pytest.fixture(scope='function')
def function_additional_filters(additional_filters_client: AdditionalFiltersClient):
    request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema])
    response = additional_filters_client.create_additional_filters_api(request=request)
    return AdditionalFilterFixture(request=request)


@pytest.fixture(scope='function')
def function_additional_filters_for_delete(additional_filters_client: AdditionalFiltersClient):
    request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema(direction='Src+Dst',
                                                                                  group_id='1',
                                                                                  ip="1.1.1.1",
                                                                                  type='pass')])
    response = additional_filters_client.create_additional_filters_api(request=request)
    return AdditionalFilterFixture(request=request)