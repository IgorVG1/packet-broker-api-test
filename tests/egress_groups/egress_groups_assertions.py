import allure
from httpx import Response

from clients.egress_groups.egress_groups_schema import GetEgressGroupsResponseSchema, CreateEgressGroupRequestSchema, \
    UpdateEgressGroupRequestSchema
from tools.assertions.base import assert_equal, assert_equal_in_expected_list
from tools.logger import get_logger


logger = get_logger("EGRESS_GROUPS_ASSERTIONS")


@allure.step('Check create egress group response')
def assert_create_egress_group_response(actual: GetEgressGroupsResponseSchema, expected: CreateEgressGroupRequestSchema):
    """
    Проверяет, что выходная группа действительно создана.
    [200]OK

    :param actual: Фактический результат - актуальный список выходных групп.
    :param expected: Ожидаемое значение - созданная выходная группа.
    """
    logger.info('Check create egress group response')

    assert_equal(actual=actual.root[-1].group_id,
                 expected=int(expected.group_id.split(sep="-")[-1]),
                 name="groupId")

    assert_equal(actual=actual.root[-1].logic_group,
                 expected=int(expected.logic_group.split(sep="-")[-1]),
                 name="logicGroup")

    assert_equal(actual=actual.root[-1].ports[-1],
                 expected=expected.ports[-1].model_dump()['port'],
                 name="ports")


@allure.step('Check create already creating egress group response')
def assert_create_already_creating_egress_group_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Выходная группа с таким ID уже существует".

    :param response: Ответ от сервера.
    """
    logger.info('Check create already creating egress group response')

    expected_value = '"Выходная группа с таким ID уже существует"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')


@allure.step('Check update egress group response')
def assert_update_egress_group_response(actual: GetEgressGroupsResponseSchema, expected: UpdateEgressGroupRequestSchema):
    """
    Проверяет, что выходная группа действительно обновлена.
    [200]OK

    :param actual: Фактический результат - актуальный список выходных групп.
    :param expected: Ожидаемое значение - созданная и измененная выходная группа.
    """
    logger.info('Check update egress group response')

    assert_equal(actual=actual.root[0].group_id,
                 expected=int(expected.group_id.split(sep="-")[-1]),
                 name="groupId")

    assert_equal(actual=actual.root[0].logic_group,
                 expected=int(expected.logic_group.split(sep="-")[-1]),
                 name="logicGroup")

    assert_equal(actual=actual.root[0].ports[-1],
                 expected=expected.ports[-1].model_dump()['port'],
                 name="ports")


@allure.step('Check update nonexistent egress group response')
def assert_update_nonexistent_egress_group_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Такой выходной группы не существует".

    :param response: Ответ от сервера.
    """
    logger.info('Check update nonexistent egress group response')

    expected_value = ['"Такой выходной группы не существует"','"Такой логической группы не существует"']
    assert_equal_in_expected_list(equal=response.text,
                                  expected_list=expected_value,
                                  name='text')


@allure.step('Check delete nonexistent egress group response')
def assert_delete_nonexistent_egress_group_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Выходная группа для этой логической группы не сконфигурированна".

    :param response: Ответ от сервера.
    """
    logger.info('Check delete nonexistent egress group response')

    expected_value = '"Выходная группа для этой логической группы не сконфигурированна"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')