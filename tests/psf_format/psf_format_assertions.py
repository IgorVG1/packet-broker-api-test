import allure
from httpx import Response

from clients.analysis_ports.analysis_ports_schema import CreateAnalysisPortRequestSchema, \
    GetAnalysisPortsResponseSchema, UpdateAnalysisPortRequestSchema
from clients.psf_format.psf_format_schema import GetPsfFormatResponseSchema, CreatePsfFormatRequestSchema, \
    UpdatePsfFormatRequestSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger("PSF_FORMAT_ASSERTIONS")


@allure.step('Check create psf format response')
def assert_create_psf_format_response(actual: GetPsfFormatResponseSchema, expected: CreatePsfFormatRequestSchema):
    """
    Проверяет, что правило спецформата действительно добавлено.
    [200]OK

    :param actual: Фактический результат - актуальный список правил спецформата.
    :param expected: Ожидаемое значение - добавленное правило спецформата.
    """
    logger.info('Check create psf format response')

    assert_equal(actual=actual.root[-1].port,
                 expected=expected.port,
                 name="port")

    assert_equal(actual=actual.root[-1].dmac,
                 expected=expected.dmac,
                 name="dmac")

    assert_equal(actual=actual.root[-1].lid,
                 expected=expected.lid,
                 name="lid")

    assert_equal(actual=actual.root[-1].pid,
                 expected=expected.pid,
                 name="pid")


@allure.step('Check create already creating psf format response')
def assert_create_already_creating_psf_format_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Данный порт уже используется".

    :param response: Ответ от сервера.
    """
    logger.info('Check create already creating psf format response')

    expected_value = '"Данный порт уже используется"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')


@allure.step('Check update psf format response')
def assert_update_psf_format_response(actual: GetPsfFormatResponseSchema, expected: UpdatePsfFormatRequestSchema):
    """
    Проверяет, что правило спецформата действительно обновлено.
    [200]OK

    :param actual: Фактический результат - актуальный список правил спецформата.
    :param expected: Ожидаемое значение - измененное правило спецформата.
    """
    logger.info('Check update psf format response')

    assert_equal(actual=actual.root[-1].port,
                 expected=expected.port,
                 name="port")

    assert_equal(actual=actual.root[-1].dmac,
                 expected=expected.dmac,
                 name="dmac")

    assert_equal(actual=actual.root[-1].lid,
                 expected=expected.lid,
                 name="lid")

    assert_equal(actual=actual.root[-1].pid,
                 expected=expected.pid,
                 name="pid")


@allure.step('Check update nonexistent psf format response')
def assert_update_nonexistent_psf_format_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Такого правила не существует".

    :param response: Ответ от сервера.
    """
    logger.info('Check update nonexistent psf format response')

    expected_value = '"Такого правила не существует"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')