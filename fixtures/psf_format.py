import pytest
from pydantic import BaseModel

from clients.psf_format.psf_format_client import PsfFormatClient, get_psf_format_client, \
    get_unauthorized_psf_format_client, get_psf_format_session, PsfFormatSession, get_unauthorized_psf_format_session
from clients.psf_format.psf_format_schema import CreatePsfFormatRequestSchema, DeletePsfFormatRequestSchema
from fixtures.authentication import UserFixture
from tools.logger import get_logger


logger = get_logger('PSF_FORMAT_FIXTURE')


class PsfFormatFixture(BaseModel):
    request: CreatePsfFormatRequestSchema


@pytest.fixture(scope='function')
def psf_format_client(function_user: UserFixture) -> PsfFormatClient:
    return get_psf_format_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_psf_format_client() -> PsfFormatClient:
    return get_unauthorized_psf_format_client()


@pytest.fixture(scope='function')
def psf_format_session(function_user: UserFixture) -> PsfFormatSession:
    return get_psf_format_session(access_token=function_user.access_token)

@pytest.fixture(scope='function')
def unauthorised_psf_format_session() -> PsfFormatSession:
    return get_unauthorized_psf_format_session()


@pytest.fixture(scope='function')
def function_psf_format(psf_format_client: PsfFormatClient) -> PsfFormatFixture:
    """
    Фикстура для предварительного добавление правила спецформата.

    :param psf_format_client: Фикстура с подготовленным клиентом для работы с /api/psf_format/.
    :return: Pydantic-модель, хранящая в себе информацию о запросе на добавление правила спецформата.
    """
    request = CreatePsfFormatRequestSchema()
    psf_format_client.create_psf_format_api(request=request)
    return PsfFormatFixture(request=request)


@pytest.fixture(scope='function')
def function_psf_format_set_up(psf_format_session: PsfFormatSession):
    """
    Фикстура для удаления имеющегося правила спецформата перед запуском теста.

    :param psf_format_session: Фикстура с подготовленным клиентом для работы с /api/psf_format/.
    """
    request = DeletePsfFormatRequestSchema()
    psf_format_session.delete_psf_format_api(request=request)

    logger.info('[Set-up completed] : Existing psf format was deleted.')


@pytest.fixture(scope='function')
def function_psf_format_tear_down(psf_format_session: PsfFormatSession):
    """
    Фикстура для удаления созданного правила спецформата по окончании теста.

    :param psf_format_session: Фикстура с подготовленным клиентом для работы с /api/psf_format/.
    """
    yield
    request = DeletePsfFormatRequestSchema()
    psf_format_session.delete_psf_format_api(request=request)

    logger.info('[Tear-down completed] : Created psf format was deleted.')