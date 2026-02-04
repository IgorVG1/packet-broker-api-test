
import allure
from typing import List
from clients.mirroring.mirroring_schema import MirroringSchema, CreateMirroringRequestSchema, UpdateMirroringRequestSchema
from tools.assertions.base import assert_equal, assert_length, assert_equal_in_expected_list
from tools.logger import get_logger

logger = get_logger("MIRRORING_ASSERTIONS")


@allure.step('Check get mirroring list response')
def assert_get_mirroring_list_response(response_get_mirroring: MirroringSchema, request_create_mirroring: CreateMirroringRequestSchema):
    """
    Проверяет ответ статуса [200]OK на получение списка групп зеркалирования.

    :param response_get_mirroring: Фактическое значение - группа зеркалирования, полученная из списка актуальных групп после добавления новой.
    :param request_create_mirroring: Ожидаемое значение - добавленная новая группа зеркалирования.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check get mirroring list response')

    assert_equal(actual=str(response_get_mirroring.mirror_id),
                 expected=request_create_mirroring.id.split(sep="-")[-1],
                 name="mirrorId")

    assert_equal(actual=str(response_get_mirroring.ingress_id),
                 expected=request_create_mirroring.ingress_group.split(sep="-")[-1],
                 name="ingressId")

    assert_equal(actual=str(response_get_mirroring.ports[0]),
                 expected=request_create_mirroring.ports[0],
                 name="ports")


@allure.step('Check create mirroring group response')
def assert_create_mirroring_response(actual: MirroringSchema, expected: CreateMirroringRequestSchema):
    """
    Проверяет ответ статуса [200]OK на добавление новой группы зеркалирования.

    :param actual: Фактическое значение - полученный актуальный список групп зеркалирования после создания группы.
    :param expected: Ожидаемое значение - новая добавленная группа зеркалирования.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create mirroring group response')

    assert_equal(actual=str(actual.mirror_id),
                 expected=expected.id.split(sep="-")[-1],
                 name="mirrorId")

    assert_equal(actual=str(actual.ingress_id),
                 expected=expected.ingress_group.split(sep="-")[-1],
                 name="ingressId")

    assert_equal(actual=actual.ports[0],
                 expected=expected.ports[0],
                 name="ports")


@allure.step('Check update mirroring group response')
def assert_update_mirroring_response(actual: MirroringSchema, expected: UpdateMirroringRequestSchema):
    """
    Проверяет ответ статуса [200]OK на изменение группы зеркалирования.

    :param actual: Фактическое значение - полученный актуальный список групп зеркалирования после внесения изменений.
    :param expected: Ожидаемое значение - измененная группа зеркалирования.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check update mirroring group response')

    assert_equal(actual=str(actual.mirror_id),
                 expected=expected.id.split(sep="-")[-1],
                 name="mirrorId")

    assert_equal(actual=str(actual.ingress_id),
                 expected=expected.ingress_group.split(sep="-")[-1],
                 name="ingressId")

    assert_equal(actual=actual.ports[0],
                 expected=expected.ports[0],
                 name="ports")


@allure.step('Check delete mirroring group response')
def assert_delete_mirroring_response(actual_mirroring_list: list[MirroringSchema]):
    """
    Проверяет ответ статуса [200]OK на удаление группы зеркалирования.

    :param actual_mirroring_list: Фактическое значение - полученный актуальный список групп зеркалирования после удаления.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check delete mirroring group response')

    assert_length(actual=actual_mirroring_list,
                  expected=[],
                  name="mirroring list")


@allure.step('Check create already creating mirroring group response')
def assert_create_already_creating_mirroring_group_response(response_text: str):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Такая группа зеркалирования уже существует".

    :param response_text: Ответ от сервера в соответствии с моделью ErrorCustomConfigResponseSchema.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check create already creating mirroring group response')
    expected_values: List[str] = [
        '"Такая группа зеркалирования уже существует"',
        '"Данная группа зеркалирования имеет правила фильтрации зеркалирования"'
    ]
    assert_equal_in_expected_list(equal=response_text,
                                  expected_list=expected_values ,
                                  name='text')


@allure.step('Check change (update/delete) nonexistent mirroring group response')
def assert_change_nonexistent_mirroring_group_response(response_text: str):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Такой группы зеркалирования не существует".

    :param response_text: Ответ от сервера в соответствии с моделью ErrorCustomConfigResponseSchema.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info('Check change (update/delete) nonexistent mirroring group response')

    assert_equal(actual=response_text,
                 expected='"Такой группы зеркалирования не существует"',
                 name='text')