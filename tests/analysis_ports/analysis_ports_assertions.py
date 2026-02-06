import allure
from httpx import Response

from clients.analysis_ports.analysis_ports_schema import CreateAnalysisPortRequestSchema, \
    GetAnalysisPortsResponseSchema, UpdateAnalysisPortRequestSchema
from clients.egress_groups.egress_groups_schema import GetEgressGroupsResponseSchema, CreateEgressGroupRequestSchema, \
    UpdateEgressGroupRequestSchema
from tools.assertions.base import assert_equal, assert_equal_in_expected_list
from tools.logger import get_logger


logger = get_logger("ANALYSIS_PORTS_ASSERTIONS")


@allure.step('Check create analysis port response')
def assert_create_analysis_port_response(actual: GetAnalysisPortsResponseSchema, expected: CreateAnalysisPortRequestSchema):
    """
    Проверяет, что порт анализа действительно создан.
    [200]OK

    :param actual: Фактический результат - актуальный список портов анализа.
    :param expected: Ожидаемое значение - созданный порт анализа.
    """
    logger.info('Check create analysis port response')

    assert_equal(actual=actual.root[-1].ingress_id,
                 expected=int(expected.ingress_group.split(sep='-')[-1]),
                 name="ingressGroup")

    assert_equal(actual=actual.root[-1].egress_port,
                 expected=expected.ports[0],
                 name="ports")


@allure.step('Check create already creating analysis port response')
def assert_create_already_creating_analysis_port_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Порт анализа на эту входную группу уже настроен".

    :param response: Ответ от сервера.
    """
    logger.info('Check create already creating analysis port response')

    expected_value = '"Порт анализа на эту входную группу уже настроен"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')


@allure.step('Check update analysis port response')
def assert_update_analysis_port_response(actual: GetAnalysisPortsResponseSchema, expected: UpdateAnalysisPortRequestSchema):
    """
    Проверяет, что порт анализа действительно обновлен.
    [200]OK

    :param actual: Фактический результат - актуальный список портов анализа.
    :param expected: Ожидаемое значение - созданный и измененный порт анализа.
    """
    logger.info('Check update analysis port response')

    assert_equal(actual=actual.root[-1].ingress_id,
                 expected=int(expected.ingress_group.split(sep='-')[-1]),
                 name="ingressGroup")

    assert_equal(actual=actual.root[-1].egress_port,
                 expected=expected.ports[0],
                 name="ports")


@allure.step('Check update nonexistent analysis port response')
def assert_update_nonexistent_analysis_port_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Порт анализа не сконфигурирован".

    :param response: Ответ от сервера.
    """
    logger.info('Check update nonexistent analysis port response')

    expected_value = '"Порт анализа не сконфигурирован"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')


@allure.step('Check delete nonexistent analysis port response')
def assert_delete_nonexistent_analysis_port_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Нет такого порта анализа".

    :param response: Ответ от сервера.
    """
    logger.info('Check delete nonexistent analysis port response')

    expected_value = '"Нет такого порта анализа"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')