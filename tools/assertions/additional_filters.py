import allure

from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    CreateAdditionalFiltersResponseSchema
from tools.logger import get_logger


logger = get_logger('ADDITIONAL_FILTERS')


@allure.step('Check create additional filters response')
def assert_create_additional_filters_response(request: CreateAdditionalFiltersRequestSchema, response: CreateAdditionalFiltersResponseSchema):
    """
    Проверяет, что ответ на создание файла соответствует запросу.

    :param request: Исходный запрос на создание файла.
    :param response: Ответ API с данными файла.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    ...