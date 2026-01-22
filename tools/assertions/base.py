import allure
from typing import Any, Sized
from tools.logger import get_logger

logger = get_logger('BASE_ASSERTIONS')


@allure.step('Check response status code equals to {expected}')
def assert_status_code(actual: int, expected: int):
    """
    Проверяет, что фактический статус-код ответа соответствует ожидаемому.

    :param actual: Фактический статус-код ответа.
    :param expected: Ожидаемый статус-код.
    :raises AssertionError: Если статус-коды не совпадают.
    """
    logger.info('Check response status code equals to "{expected}"')
    assert actual == expected, \
        (
            'Incorrect response status code.'
            f'\nExpected status code:   "{expected}"'
            f'Actual status code:       "{actual}"'
        )


@allure.step('Check object: {name} - equals to {expected}')
def assert_equal(actual: Any, expected: Any, name: str):
    """
    Проверяет, что фактическое значение равно ожидаемому.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение.
    :raises AssertionError: Если фактическое значение не равно ожидаемому.
    """
    logger.info(f'Check object: "{name}" - equals to "{expected}"')
    assert actual == expected, \
        (
            f'Incorrect value:  "{name}"'
            f'\nExpected value: "{expected}"'
            f'Actual value:     "{actual}"'
        )

def assert_is_true(actual: Any, name: str):
    """
    Проверяет, что фактическое значение является истинным.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :raise
    """
    logger.info(f'Check "{name}" is true')
    assert actual, \
        (
            f'Incorrect value: "{name}"'
            f'\nExpected true value, but actual: "{actual}"'
        )

def assert_length(actual: Sized, expected: Sized, name: str):
    """
    Проверяет, что длины двух объектов совпадают.

    :param name: Название проверяемого объекта.
    :param actual: Фактический объект.
    :param expected: Ожидаемый объект.
    :raises AssertionError: Если длины не совпадают.
    """
    with allure.step(f'Check length of "{name}" equals to "{len(expected)}"'):
        logger.info(f'Check length of "{name}" equals to {len(expected)}')

        assert len(actual) == len(expected), \
            (
                f'Incorrect object length: "{name}" .'
                f'Expected length: "{len(expected)}". '
                f'Actual length: "{len(actual)}".'
            )