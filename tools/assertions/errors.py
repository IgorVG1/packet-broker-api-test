import allure

from clients.errors_schema import ValidationErrorResponseSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger('ERRORS_ASSERTIONS')


@allure.step('Check validation error response')
def assert_error_for_not_authenticated_user(response: ValidationErrorResponseSchema):
    """
    Проверяет структуру ошибки выполнения запроса от неаутентифицированного пользователя.
    [403]FORBIDDEN - Учетные данные не были предоставлены.

    :param response: Ответ API в формате JSON.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check validation error response')
    expected_value = "Учетные данные не были предоставлены."
    assert_equal(actual=response.detail,
                 expected=expected_value,
                 name='detail')