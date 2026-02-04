import allure
from httpx import Response
from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger("NODES_ASSERTIONS")


@allure.step('Check apply invalid nodes config response')
def assert_apply_invalid_nodes_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Неверная конфигурация. Задайте признак отбора".

    :param response: Ответ от сервера.
    """
    logger.info('Check apply invalid nodes config response')

    expected_value = '"Неверная конфигурация. Задайте признак отбора"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')