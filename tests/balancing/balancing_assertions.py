import allure

from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger('BALANCING_ASSERTIONS')


@allure.step('Check create balancing for created balancing group response')
def assert_create_balancing_for_created_balancing_group_response(response_str: str):
    """
    Проверяет структуру предупреждения о создании балансировки для УЖЕ сконфигурированной группы.
    [412]PRECONDITION_FAILED - Балансировка для этой логической группы уже сконфигурирована

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create balancing for created balancing group response')

    expected_value = '"Балансировка для этой логической группы уже сконфигурирована"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')


@allure.step('Check create balancing response without logicId')
def assert_create_balancing_without_logic_id_response(response_str: str):
    """
    Проверяет структуру предупреждения о попытке создании балансировки без logicId.
    [412]PRECONDITION_FAILED - Неправильно задан ID логической группы

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create balancing response without logicId')

    expected_value = '"Неправильно задан ID логической группы"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')


@allure.step('Check create balancing response without balanceType')
def assert_create_balancing_without_balance_type_response(response_str: str):
    """
    Проверяет структуру предупреждения о попытке создании балансировки без balanceType.
    [412]PRECONDITION_FAILED - Неправильно указан тип балансировки

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create balancing response without balanceType')

    expected_value = '"Неправильно указан тип балансировки"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')


@allure.step('Check update balancing response without logicId')
def assert_update_balancing_without_logic_id_response(response_str: str):
    """
    Проверяет структуру предупреждения о попытке изменения балансировки без logicId.
    [412]PRECONDITION_FAILED - Неправильно задан ID логической группы

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check update balancing response without logicId')

    expected_value = '"Неправильно задан ID логической группы"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')


@allure.step('Check update balancing response without balanceType')
def assert_update_balancing_without_balance_type_response(response_str: str):
    """
    Проверяет структуру предупреждения о попытке изменения балансировки без balanceType.
    [412]PRECONDITION_FAILED - Неправильно указан тип балансировки

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check update balancing response without balanceType')

    expected_value = '"Неправильно указан тип балансировки"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')


@allure.step('Check response of delete balancing that had been deleted ')
def assert_delete_had_been_deleted_balancing(response_str: str):
    """
    Проверяет структуру предупреждения о попытке удаления уже удаленной группы балансировки.
    [412]PRECONDITION_FAILED - В данной логической группе не задана балансировка

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check response of delete balancing that had been deleted')

    expected_value = '"В данной логической группе не задана балансировка"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')


@allure.step('Check response of delete without logicGroup')
def assert_delete_without_logic_group_response(response_str: str):
    """
    Проверяет структуру предупреждения о попытке удаления без указания logicGroup.
    [412]PRECONDITION_FAILED - Некорреткный ID логической группы

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check response of delete without logicGroup')

    expected_value = '"Некорреткный ID логической группы"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')