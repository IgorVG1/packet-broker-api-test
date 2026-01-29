import allure
from httpx import Response

from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("CUSTOM_CONFIG_ASSERTIONS")


@allure.step('Check download custom config response')
def assert_download_custom_config_response(response: Response):
    """
    Проверяет, что в ответе от сервера получен файл.
    [200]OK

    :param response: Ответ от сервера в виде объекта httpx.Response.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check download custom config response')

    assert_equal(actual=type(response.content),
                 expected=bytes,
                 name='content-type')


@allure.step('Check upload broken custom config response')
def assert_upload_broken_custom_config(response_text: str):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - Unexpected error: ...

    :param response_text: Ответ от сервера в соответствии с моделью ErrorCustomConfigResponseSchema.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check upload broken custom config response')

    assert_equal(actual=response_text,
                 expected='"Unexpected error: <class \'ValueError\'>invalid literal for int() with base 10: \'ABDC\'"',
                 name='text')