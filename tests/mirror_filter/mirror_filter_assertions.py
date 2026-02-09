import allure
from httpx import Response

from clients.mirror_filter.mirror_filter_schema import CreateMirrorFilterRequestSchema, GetMirrorFilterListResponseSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger


logger = get_logger("MIRROR_FILTER_ASSERTIONS")


@allure.step('Check create mirror filter response')
def assert_create_mirror_filter_response(actual: GetMirrorFilterListResponseSchema, expected: CreateMirrorFilterRequestSchema):
    """
    Проверяет, что правило фильтрации зеркалирования действительно добавлено.
    [200]OK

    :param actual: Фактический результат - актуальный список правил фильтрации зеркалирования.
    :param expected: Ожидаемое значение - добавленное правило фильтрации зеркалирования.
    """
    logger.info('Check create mirror filter response')

    assert_equal(actual=actual.root[-1].ig_md_dst_addr.value,
                 expected=expected.root[0].new_ip_dst,
                 name="newIpDst")

    assert_equal(actual=int(actual.root[-1].ig_md_dst_addr.mask.split(sep='/')[-1]),
                 expected=expected.root[0].new_ip_dst_mask,
                 name="newIpDstMask")

    assert_equal(actual=actual.root[-1].ig_md_src_addr.value,
                 expected=expected.root[0].new_ip_src,
                 name="newIpSrc")

    assert_equal(actual=int(actual.root[-1].ig_md_src_addr.mask.split(sep='/')[-1]),
                 expected=expected.root[0].new_ip_src_mask,
                 name="newIpSrcMask")

    assert_equal(actual=actual.root[-1].dest_num,
                 expected=expected.root[0].dest_num,
                 name="destNum")

    assert_equal(actual=actual.root[-1].ingress_group,
                 expected=expected.root[0].ingress_group,
                 name="ingressGroup")

    assert_equal(actual=actual.root[-1].mirror_group,
                 expected=expected.root[0].mirror_group,
                 name="mirrorGroup")

    assert_equal(actual=actual.root[-1].traffic_type,
                 expected=expected.root[0].traffic_type,
                 name="trafficType")


@allure.step('Check delete nonexistent mirror filter response')
def assert_delete_nonexistent_mirror_filter_response(response: Response):
    """
    Проверяет, что в ответе от сервера об ошибке соответствует структуре.
    [412]PRECONDITION_FAILED - "Нет такого правила фильтрации зеркалирования".

    :param response: Ответ от сервера.
    """
    logger.info('Check delete nonexistent mirror filter response')

    expected_value = '"Нет такого правила фильтрации зеркалирования"'
    assert_equal(actual=response.text,
                 expected=expected_value,
                 name='text')