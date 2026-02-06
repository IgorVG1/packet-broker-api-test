import pytest
from pydantic import BaseModel

from clients.analysis_ports.analysis_ports_client import AnalysisPortsClient, get_analysis_ports_client, \
    get_unauthorised_analysis_ports_client, AnalysisPortsSession, get_analysis_ports_session, \
    get_unauthorised_analysis_ports_session
from clients.analysis_ports.analysis_ports_schema import CreateAnalysisPortRequestSchema, \
    DeleteAnalysisPortRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('ANALYSIS_PORTS_FIXTURE')


class AnalysisPortsFixture(BaseModel):
    request: CreateAnalysisPortRequestSchema


@pytest.fixture(scope='function')
def analysis_ports_client(function_user: UserFixture) -> AnalysisPortsClient:
    return get_analysis_ports_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_analysis_ports_client() -> AnalysisPortsClient:
    return get_unauthorised_analysis_ports_client()


@pytest.fixture(scope='function')
def analysis_ports_session(function_user: UserFixture) -> AnalysisPortsSession:
    return get_analysis_ports_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorised_analysis_ports_session() -> AnalysisPortsSession:
    return get_unauthorised_analysis_ports_session()


@pytest.fixture(scope='function')
def function_analysis_port(analysis_ports_client: AnalysisPortsClient) -> AnalysisPortsFixture:
    """
    Фикстура для предварительного создания порта анализа.

    :param analysis_ports_client: Фикстура с подготовленным клиентом для работы с /api/unknown/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на создание порта анализа.
    """
    request = CreateAnalysisPortRequestSchema()
    analysis_ports_client.create_analysis_port_api(request=request)
    return AnalysisPortsFixture(request=request)


@pytest.fixture(scope='function')
def function_analysis_port_set_up(analysis_ports_session: AnalysisPortsSession):
    """
    Фикстура для удаления имеющегося порта анализа перед запуском теста.

    :param analysis_ports_session: Фикстура с подготовленным клиентом для работы с /api/unknown/.
    """
    request = DeleteAnalysisPortRequestSchema()
    analysis_ports_session.delete_analysis_port_api(request=request)

    logger.info('[Set-up completed] : Existing analysis port was deleted.')


@pytest.fixture(scope='function')
def function_analysis_port_tear_down(analysis_ports_session: AnalysisPortsSession):
    """
    Фикстура для удаления созданного порта анализа по окончании теста.

    :param analysis_ports_session: Фикстура с подготовленным клиентом для работы с /api/unknown/.
    """
    yield
    request = DeleteAnalysisPortRequestSchema()
    analysis_ports_session.delete_analysis_port_api(request=request)

    logger.info('[Tear-down completed] : Created analysis port was deleted.')