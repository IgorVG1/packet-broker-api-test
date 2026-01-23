import pytest
from pydantic import BaseModel
from clients.additional_filters.additional_filters_client import AdditionalFiltersClient, get_additional_filters_client, \
    AdditionalFiltersSession, get_additional_filters_session
from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    CreateAdditionalFiltersSchema
from fixtures.authentication import UserFixture


class DeleteAdditionalFiltersData(BaseModel):
    """
    Описание структуры pydantic-model с данными дополнительного фильтра для его удаления.
    Attributes:
        direction: str
        group_id: str
        ip: str
        type: str
    """
    direction: str
    group_id: str
    ip: str
    type: str


class AdditionalFilterFixture(BaseModel):
    request: CreateAdditionalFiltersRequestSchema
    response: DeleteAdditionalFiltersData


@pytest.fixture(scope='function')
def additional_filters_client(function_user: UserFixture) -> AdditionalFiltersClient:
    return get_additional_filters_client(user=function_user.authentication_user)


@pytest.fixture(scope='function')
def additional_filters_session(function_user: UserFixture) -> AdditionalFiltersSession:
    return get_additional_filters_session(access_token=function_user.access_token)


@pytest.fixture(scope='function')
def function_additional_filters(additional_filters_client: AdditionalFiltersClient):
    request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema])
    response = additional_filters_client.create_additional_filters_api(request=request)
    return AdditionalFilterFixture(request=request)


@pytest.fixture(scope='function')
def function_additional_filters_for_delete(additional_filters_client: AdditionalFiltersClient):
    test_data = DeleteAdditionalFiltersData(direction = 'Src+Dst',
                                            group_id = '1',
                                            ip = '1.1.1.1',
                                            type = 'pass')
    request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema(direction=test_data.direction,
                                                                                  group_id=test_data.group_id,
                                                                                  ip=test_data.ip,
                                                                                  type=test_data.type)])
    response = additional_filters_client.create_additional_filters_api(request=request)
    return AdditionalFilterFixture(request=request,
                                   response=test_data)