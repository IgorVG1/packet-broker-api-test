import allure, pytest

from http import HTTPStatus

from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.loopback_ports.loopback_ports_client import LoopbackPortsClient, LoopbackPortsSession
from clients.loopback_ports.loopback_ports_schema import GetLoopbackPortsResponseSchema, \
    CreateLoopbackPortsRequestSchema, DeleteLoopbackPortsRequestSchema
from config import settings
from tests.loopback_ports.loopback_ports_assertions import assert_get_loopback_ports_response, \
    assert_create_loopback_ports_response, assert_delete_loopback_ports_response, \
    assert_create_loopback_ports_with_incorrect_body
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('LOOPBACK_PORTS')


@pytest.mark.loopback_ports
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.LOOPBACK_PORTS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.LOOPBACK_PORTS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.LOOPBACK_PORTS)
class TestLoopbackPorts:

    @allure.title("[200]OK - Get loopback ports speed limit list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_loopback_ports(self,
                                function_loopback_port_set_up,
                                loopback_ports_client: LoopbackPortsClient):
        response = loopback_ports_client.get_loopback_ports_speed()
        response_data = GetLoopbackPortsResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        assert_get_loopback_ports_response(actual_loopback_ports=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Get loopback ports speed limit list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_loopback_ports_by_unauthorised_user(self, unauthorised_loopback_ports_client: LoopbackPortsClient):
        response = unauthorised_loopback_ports_client.get_loopback_ports_speed()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create loopback port speed limits")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_loopback_port(self,
                                function_loopback_port_set_up,
                                loopback_ports_client: LoopbackPortsClient,
                                function_loopback_port_tear_down):
        request = CreateLoopbackPortsRequestSchema()
        response_create = loopback_ports_client.create_loopback_ports(request=request)

        response_get = loopback_ports_client.get_loopback_ports_speed()
        response_get_data = GetLoopbackPortsResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response_create.status_code,
                           expected=HTTPStatus.OK)
        assert_create_loopback_ports_response(actual_loopback_ports=response_get_data,
                                              expected_loopback_ports=request)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Create loopback port speed limits by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_loopback_port_by_unauthorised_user(self, unauthorised_loopback_ports_client: LoopbackPortsClient):
        request = CreateLoopbackPortsRequestSchema()
        response = unauthorised_loopback_ports_client.create_loopback_ports(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Delete loopback port speed limits")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_loopback_port(self,
                                   function_loopback_port,
                                   loopback_ports_session: LoopbackPortsSession,
                                   loopback_ports_client: LoopbackPortsClient):
        request = DeleteLoopbackPortsRequestSchema()
        response_delete = loopback_ports_session.delete_loopback_ports(request=request)

        response_get = loopback_ports_client.get_loopback_ports_speed()
        response_get_data = GetLoopbackPortsResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response_delete.status_code,
                           expected=HTTPStatus.OK)
        assert_delete_loopback_ports_response(actual_loopback_ports=response_get_data)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Delete loopback port speed limits by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_loopback_port_by_unauthorised_user(self, unauthorised_loopback_ports_session: LoopbackPortsSession):
        request = DeleteLoopbackPortsRequestSchema()
        response = unauthorised_loopback_ports_session.delete_loopback_ports(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())