import allure
from httpx import Response
from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger("INGRESS_GROUPS_ASSERTIONS")


@allure.step('Check create already creating ingress group response')
def assert_create_already_creating_ingress_group_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Такая группа зеркалирования уже существует".

    :param response: Ответ от сервера.
    """
    logger.info('Check create already creating ingress group response')

    expected_value = '"Входная группа с таким ID уже существует"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')


@allure.step('Check update nonexistent ingress group response')
def assert_update_nonexistent_ingress_group_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Такой входной группы не существует".

    :param response: Ответ от сервера.
    """
    logger.info('Check update nonexistent ingress group response')

    expected_value = '"Такой входной группы не существует"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')


@allure.step('Check delete nonexistent ingress group response')
def assert_delete_nonexistent_ingress_group_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "L1 - данный порт не является портом входной группы".

    :param response: Ответ от сервера.
    """
    logger.info('Check delete nonexistent ingress group response')

    expected_value = '"L1 - данный порт не является портом входной группы"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')