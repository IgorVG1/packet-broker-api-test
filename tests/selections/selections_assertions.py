import allure
from httpx import Response
from clients.selections.selections_schema import GetSelectionsResponseSchema, CreateSelectionRequestSchema
from tools.assertions.base import assert_equal, assert_equal_not_in_list
from tools.logger import get_logger

logger = get_logger("SELECTIONS_ASSERTIONS")


@allure.step('Check get selections list response')
def check_get_selections_list_response(actual: GetSelectionsResponseSchema, expected: CreateSelectionRequestSchema):
    """
    Проверяет ответ статуса [200]OK на получение списка групп отбора.

    :param actual: Фактическое значение - актуальный список групп отбора.
    :param expected: Ожидаемое значение - добавленная новая группа отбора.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check get selections list response')

    selection = actual.root[-1]

    assert_equal(actual=int(expected.ingress_id.split(sep="-")[-1]),
                 expected=selection.ingress_id,
                 name="ingressId")

    assert_equal(actual=int(expected.logic_id.split(sep="-")[-1]),
                 expected=selection.logic_id,
                 name="logicId")

    assert_equal(actual=expected.selection.ip_protocol,
                 expected=selection.ip_protocol,
                 name="ipProtocol")

    assert_equal(actual=expected.selection.traffic_type,
                 expected=selection.traffic_type,
                 name="trafficType")

    assert_equal(actual=expected.selection.src_port,
                 expected=selection.src_port,
                 name="srcPort")

    assert_equal(actual=expected.selection.dst_port,
                 expected=selection.dst_port,
                 name="dstPort")


@allure.step('Check create selection group response')
def check_create_selection_group_response(actual: GetSelectionsResponseSchema, expected: CreateSelectionRequestSchema):
    """
    Проверяет ответ статуса [200]OK на создание группы отбора.

    :param actual: Фактическое значение - актуальный список групп отбора.
    :param expected: Ожидаемое значение - добавленная новая группа отбора.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create selection group response')

    selection = actual.root[-1]

    assert_equal(actual=int(expected.ingress_id.split(sep="-")[-1]),
                 expected=selection.ingress_id,
                 name="ingressId")

    assert_equal(actual=int(expected.logic_id.split(sep="-")[-1]),
                 expected=selection.logic_id,
                 name="logicId")

    assert_equal(actual=expected.selection.ip_protocol,
                 expected=selection.ip_protocol,
                 name="ipProtocol")

    assert_equal(actual=expected.selection.traffic_type,
                 expected=selection.traffic_type,
                 name="trafficType")

    assert_equal(actual=expected.selection.src_port,
                 expected=selection.src_port,
                 name="srcPort")

    assert_equal(actual=expected.selection.dst_port,
                 expected=selection.dst_port,
                 name="dstPort")


@allure.step('Check create already creating selection group response')
def assert_create_already_creating_selection_group_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Логическая группа с таким ID уже существует".

    :param response: Ответ от сервера.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create already creating selection group response')

    assert_equal(actual=response.text,
                 expected='"Логическая группа с таким ID уже существует"',
                 name='text')


@allure.step('Check delete selection group response')
def check_delete_selection_group_response(selections_list_before: GetSelectionsResponseSchema, selections_list_after: GetSelectionsResponseSchema):
    """
    Проверяет ответ статуса [200]OK на создание группы отбора.

    :param selections_list_before: Список групп отбора до удаления тестовой группы отбора.
    :param selections_list_after: Список групп отбора после удаления тестовой группы отбора.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check delete selection group response')

    assert_equal_not_in_list(equal=selections_list_before.root[-1],
                             list=selections_list_after.root,
                             name='selection list')


@allure.step('Check delete selection group with incorrect body')
def check_delete_selection_group_with_incorrect_body_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Неверно задан идентификатор входной группы".

    :param response: Ответ от сервера.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check delete selection group with incorrect body')

    assert_equal(actual=response.text,
                 expected='"Неверно задан идентификатор входной группы"',
                 name='text')