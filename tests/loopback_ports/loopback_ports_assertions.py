import math

import allure

from httpx import Response

from clients.loopback_ports.loopback_ports_schema import GetLoopbackPortsResponseSchema, \
    CreateLoopbackPortsRequestSchema
from clients.ports.ports_schema import CreatePortRequestSchema, ConfiguredPortSchema, GetPossiblePortsListResponse
from tools.assertions.base import assert_equal, assert_equal_in_expected_list_no_logs
from tools.logger import get_logger
from tests.ports.ports_data import POSSIBLE_PORTS

logger = get_logger("LOOPBACK_PORTS_ASSERTIONS")


@allure.step('Check get list loopback ports speed limits response')
def assert_get_loopback_ports_response(actual_loopback_ports: GetLoopbackPortsResponseSchema):
    """
    Проверяет ответ на запрос получения ограничений скоростей loopback портов.

    :param actual_loopback_ports: Список текущих ограничений скоростей loopback портов.
    :raises AssertionError: Если хоть один параметр не совпадает.
    """
    logger.info('Check get list loopback ports speed limits response')

    for speed_limit in actual_loopback_ports.root:
        assert_equal(actual=speed_limit.speed_limit,
                     expected=None,
                     name="speedLimit")


@allure.step('Check create loopback ports speed limits response')
def assert_create_loopback_ports_response(actual_loopback_ports: GetLoopbackPortsResponseSchema, expected_loopback_ports: CreateLoopbackPortsRequestSchema):
    """
    Проверяет ответ на запрос о назначении ограничения скорости loopback портов.

    :param actual_loopback_ports: Список текущих ограничений скоростей loopback портов.
    :param expected_loopback_ports: Список назначенных ограничений скоростей loopback портов.
    :raises AssertionError: Если хоть один параметр не совпадает.
    """
    logger.info('Check create loopback ports speed limits response')

    for index, expected_loopback_port in enumerate(expected_loopback_ports.root):

        assert_equal(actual=actual_loopback_ports.root[index].port,
                     expected=expected_loopback_port.port,
                     name="port")

        assert_equal(actual=math.ceil((actual_loopback_ports.root[index].speed_limit)*1004),
                     expected=expected_loopback_port.speed_limit,
                     name="speedLimit")


@allure.step('Check create loopback ports speed limits with incorrect body')
def assert_create_loopback_ports_with_incorrect_body(response: Response):
    """
    Проверяет ответ на некорректный запрос о назначении ограничения скорости loopback портов.
    [412] Precondition Failed.

    :param response: Ответ от сервера о безуспешной попытке создания порта с некорректными данными.
    """
    logger.info('Check create loopback ports speed limits with incorrect body')

    assert_equal(actual=response.text,
                 expected='"Не удалось прочитать запрос. Неверно сконфигурирован JSON"',
                 name="text")


@allure.step('Check delete loopback ports speed limits response')
def assert_delete_loopback_ports_response(actual_loopback_ports: GetLoopbackPortsResponseSchema):
    """
    Проверяет ответ на запрос получения ограничений скоростей loopback портов.

    :param actual_loopback_ports: Список текущих ограничений скоростей loopback портов.
    :raises AssertionError: Если хоть один параметр не совпадает.
    """
    logger.info('Check delete loopback ports speed limits response')

    for actual_loopback_port in actual_loopback_ports.root:

        assert_equal(actual=actual_loopback_port.speed_limit,
                     expected=None,
                     name="speedLimit")




@allure.step('Check response of create port with incorrect body')
def assert_create_port_with_incorrect_body(response: Response):
    """
    Проверяет, что сконфигурированный новый порт сохранился в актуальном списке на коммутаторе.
    [412] Precondition Failed.

    :param response: Ответ от сервера о безуспешной попытке создания порта с некорректными данными.
    """
    logger.info('Check response of create port with incorrect body')

    expected_text = '"Неверно заданы поля JSON. Запрос некорректен"'
    assert_equal(actual=response.text,
                 expected=expected_text,
                 name='text')


@allure.step('Check response of update nonexistent port')
def assert_update_nonexistent_port(response: Response):
    """
    Проверяет, что в ответ на запрос об обновлении несуществующего порта приходит ошибка.
    [412] Precondition Failed.

    :param response: Ответ от сервера о безуспешной попытке создания порта с некорректными данными.
    """
    logger.info('Check response of update nonexistent port')

    expected_text = '"Такого порта не существует"'
    assert_equal(actual=response.text,
                 expected=expected_text,
                 name='text')


@allure.step('Check deleted port does not exist')
def assert_deleted_port_not_exist(response: ConfiguredPortSchema):
    """
    Проверяем, что после выполнения запроса на удаление в списке портов данные порты отсутствуют.
    :param response: Проверяемый порт.
    """
    logger.info('Check deleted port does not exist')
    assert response.port != "1/0"


@allure.step('Check deletes port with incorrect body')
def assert_delete_port_with_incorrect_body(response: Response):
    """
    Проверяем обработку ошибки [412]PRECONDITION_FAILED с помощью отправки запроса на удаление без тела запроса.
    :param response: Ответ от сервера с ошибкой [412].
    """
    logger.info('Check deletes port with incorrect body')
    assert_equal(actual=response.text,
                 expected='"Не удалось прочитать запрос. Неверно сконфигурирован JSON"',
                 name='text')


@allure.step('Check possible ports list')
def assert_possible_ports_list(actual_possible_ports_list: GetPossiblePortsListResponse):
    """
    Проверяем обработку ошибки [412]PRECONDITION_FAILED с помощью отправки запроса на удаление без тела запроса.
    :param actual_possible_ports_list: Фактическое значение - Список доступных портов, полученных в ответе от сервера.
    """
    logger.info('Check possible ports list')

    for port in POSSIBLE_PORTS:
        assert_equal_in_expected_list_no_logs(equal=port,
                                              expected_list=actual_possible_ports_list.root,
                                              name=f'Port {port}')