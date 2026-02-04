import pytest
from pydantic import BaseModel
from clients.selections.selections_client import SelectionsClient, get_selections_client, \
    get_unauthorised_selections_client, SelectionsSession, get_selections_session, get_unauthorised_selections_session
from clients.selections.selections_schema import CreateSelectionRequestSchema, DeleteSelectionRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('SELECTIONS_FIXTURE')


class SelectionFixture(BaseModel):
    request: CreateSelectionRequestSchema


@pytest.fixture(scope='function')
def selections_client(function_user: UserFixture) -> SelectionsClient:
    return get_selections_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_selections_client() -> SelectionsClient:
    return get_unauthorised_selections_client()


@pytest.fixture(scope='function')
def selections_session(function_user: UserFixture) -> SelectionsSession:
    return get_selections_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorised_selections_session() -> SelectionsSession:
    return get_unauthorised_selections_session()


@pytest.fixture(scope='function')
def function_selection(selections_client: SelectionsClient) -> SelectionFixture:
    """
    Фикстура для предварительного создания группы отбора.

    :param selections_client: Фикстура с подготовленным клиентом для работы с /api/selections/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на создание группы отбора.
    """
    request = CreateSelectionRequestSchema()
    selections_client.create_selection_api(request=request)
    return SelectionFixture(request=request)


@pytest.fixture(scope='function')
def function_selection_set_up(selections_session: SelectionsSession):
    """
    Фикстура для удаления созданной группы отбора перед запуском теста.

    :param selections_session: Фикстура с подготовленной сессией для работы с /api/selections/.
    """
    request = DeleteSelectionRequestSchema()
    selections_session.delete_selection_api(request=request)

    logger.info('[Tear-down completed] : Created selection group was deleted.')


@pytest.fixture(scope='function')
def function_selection_tear_down(selections_session: SelectionsSession):
    """
    Фикстура для удаления группы отбора по окончании теста.

    :param selections_session: Фикстура с подготовленным клиентом для работы с /api/selections/.
    """
    yield
    request = DeleteSelectionRequestSchema()
    selections_session.delete_selection_api(request=request)

    logger.info('[Tear-down completed] : Created selection group was deleted.')