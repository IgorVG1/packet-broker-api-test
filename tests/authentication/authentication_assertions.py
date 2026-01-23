import allure

from clients.authentication.authentication_schema import InvalidLoginResponseSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger('AUTHENTICATION_ASSERTIONS')


@allure.step('Check create additional filters response')
def assert_invalid_log_in_response(response: InvalidLoginResponseSchema):
    """
    Проверяет структуру предупреждения о некорректном создании дополнительного фильтра.
    [412]PRECONDITION_FAILED - Не указано направление правила дополнительной фильтрации

    :param response: Ответ API строкового типа.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    expected = "user not found"
    assert_equal(actual=response.detail,
                 expected=expected,
                 name='detail')