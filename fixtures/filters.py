import pytest
from pydantic import BaseModel
from clients.filters.filters_client import FiltersClient, FiltersSession, get_filters_client, get_filters_session, \
    get_unauthorised_filters_client, get_unauthorised_filters_session
from clients.filters.filters_schema import CreateFiltersRequestSchema, CreateFilterSchema
from fixtures.authentication import UserFixture
from tests.filters.filters_data import FILTERS_FOR_DELETE


class FiltersFixture(BaseModel):
    request: CreateFilterSchema


@pytest.fixture(scope='function')
def filters_client(function_user: UserFixture) -> FiltersClient:
    return get_filters_client(user=function_user.authentication_user)


@pytest.fixture(scope='function')
def unauthorised_filters_client() -> FiltersClient:
    return get_unauthorised_filters_client()


@pytest.fixture(scope='function')
def filters_session(function_user: UserFixture) -> FiltersSession:
    return get_filters_session(access_token=function_user.access_token)


@pytest.fixture(scope='function')
def unauthorised_filters_session() -> FiltersSession:
    return get_unauthorised_filters_session()


@pytest.fixture(scope='function')
def function_filters(filters_client: FiltersClient) -> FiltersFixture:
    """
    Фикстура для предварительного создания фильтров.

    :param filters_client: Фикстура с подготовленным клиентом для работы с /api/filters/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на загрузку конфигурации.
    """
    request = CreateFilterSchema()
    filters_client.create_filters_api(request=request)
    return FiltersFixture(request=request)


@pytest.fixture(scope='function')
def function_filters_tear_down(filters_session: FiltersSession):
    """
    Фикстура для удаления созданных фильтров по окончании теста.

    :param filters_session: Фикстура с подготовленной сессией для работы с /api/filters/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на загрузку конфигурации.
    """
    yield
    request = FILTERS_FOR_DELETE.model_dump(by_alias=True)
    filters_session.delete_filters_api(request=request)