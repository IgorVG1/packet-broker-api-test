from typing import List

import allure

from httpx import Response
from clients.ports.ports_schema import CreatePortRequestSchema, ConfiguredPortSchema, GetPossiblePortsListResponse
from tools.assertions.base import assert_equal, assert_equal_in_expected_list, assert_equal_in_expected_list_no_logs
from tools.logger import get_logger
from tests.ports.ports_data import POSSIBLE_PORTS

logger = get_logger("PORTS_ASSERTIONS")


@allure.step('Check status created port')
def assert_port(actual_port: ConfiguredPortSchema, expected_port: CreatePortRequestSchema):
    """
    Проверяет, что сконфигурированный новый порт сохранился в актуальном списке на коммутаторе.

    :param actual_port: Фактическое значение - структура порта, полученного из списка запрашиваемых в тесте.
    :param expected_port: Ожидаемое значение - структура порта, созданного перед тестом.
    :raises AssertionError: Если хоть один параметр не совпадает.
    """
    logger.info('Check status created port')

    assert_equal(actual=actual_port.name,
                 expected=expected_port.name,
                 name='name')
    assert_equal(actual=actual_port.port,
                 expected=expected_port.port,
                 name='port')
    assert_equal(actual=actual_port.speed,
                 expected=expected_port.speed,
                 name='speed')
    assert_equal(actual=actual_port.mtu,
                 expected=expected_port.mtu,
                 name='mtu')
    assert_equal(actual=actual_port.an,
                 expected=expected_port.an,
                 name='an')
    assert_equal(actual=actual_port.fec,
                 expected=expected_port.fec,
                 name='fec')
    assert_equal(actual=actual_port.dir,
                 expected=expected_port.dir,
                 name='dir')
    assert_equal(actual=actual_port.loopback,
                 expected=expected_port.loopback,
                 name='loopback')
    assert_equal(actual=actual_port.reserve_port,
                 expected=expected_port.reserve_port,
                 name='reservePort')
    assert_equal(actual=actual_port.mac_dst_egress,
                 expected=expected_port.mac_dst_egress,
                 name='mac_dst_egress')


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