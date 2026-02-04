import allure

from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger('ADDITIONAL_FILTERS_ASSERTIONS')


@allure.step('Check create additional filters response')
def assert_create_additional_filters_without_direction_response(response_str: str):
    """
    Проверяет структуру предупреждения о некорректном создании дополнительного фильтра.
    [412]PRECONDITION_FAILED - Не указано направление правила дополнительной фильтрации

    :param response_str: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create additional filters response')

    expected_value = '"Не указано направление правила дополнительной фильтрации"'
    assert_equal(actual=response_str,
                 expected=expected_value,
                 name='string response')