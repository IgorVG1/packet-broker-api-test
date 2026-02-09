import allure, pytest

from http import HTTPStatus
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.ports.ports_client import PortsClient, PortsSession
from clients.ports.ports_schema import CreatePortRequestSchema, ConfiguredPortSchema, CreatePortRequest412Schema, \
    UpdatedPortSchema, DeletePortsRequestSchema, GetPossiblePortsListResponse, UpdatePortStatusRequestSchema, \
    GetAllPortsListResponse
from config import settings
from fixtures.ports import PortsFixture
from tests.ports.ports_assertions import assert_port, assert_create_port_with_incorrect_body, \
    assert_update_nonexistent_port, assert_delete_port_with_incorrect_body, \
    assert_possible_ports_list, assert_invalid_update_port_status_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('PORTS')


@pytest.mark.ports
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.PORTS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.PORTS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.PORTS)
class TestPorts:



    @allure.title("[200]OK - Get configured ports list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_ports_list(self,
                            function_ports: PortsFixture,
                            ports_client: PortsClient,
                            function_ports_tear_down):
        response = ports_client.get_ports_list_api()
        created_port = response.json()[0]
        response_data = ConfiguredPortSchema.model_validate(created_port)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_port(actual_port=response_data,
                    expected_port=function_ports.request)

        validate_json_schema(instance=created_port,
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Get configured ports list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_ports_list_by_unauthorised_user(self, unauthorised_ports_client: PortsClient):
        response = unauthorised_ports_client.get_ports_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())



    @allure.title("[200]OK - Get possible ports list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_possible_ports_list(self, ports_client: PortsClient):
        response = ports_client.get_possible_ports_list_api()
        response_data = GetPossiblePortsListResponse.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        assert_possible_ports_list(actual_possible_ports_list=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Get possible ports list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_possible_ports_list_by_unauthorised_user(self, unauthorised_ports_client: PortsClient):
        response = unauthorised_ports_client.get_possible_ports_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())



    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @allure.title("[200]OK - Create configured ports")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_port(self,
                         ports_client: PortsClient,
                         function_ports_tear_down):

        request = CreatePortRequestSchema()
        response = ports_client.create_ports_api(request=request)

        response_get_port = ports_client.get_ports_list_api().json()[0]
        created_port = ConfiguredPortSchema.model_validate(response_get_port)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_port(actual_port=created_port,
                    expected_port=request)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Create configured ports by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_port_by_unauthorised_user(self, unauthorised_ports_client: PortsClient):
        request = CreatePortRequestSchema()
        response = unauthorised_ports_client.create_ports_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Create configured ports with incorrect json in body")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_port_with_incorrect_body(self, ports_client: PortsClient):
        request = CreatePortRequest412Schema()
        response = ports_client.create_ports_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_create_port_with_incorrect_body(response=response)



    @allure.title("[200]OK - Update configured ports")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_port(self,
                         function_ports: PortsFixture,
                         ports_client: PortsClient,
                         function_ports_tear_down):
        request = UpdatedPortSchema()
        response = ports_client.update_ports_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Update ports by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_by_unauthorised_user(self, unauthorised_ports_client: PortsClient):
        request = UpdatedPortSchema()
        response = unauthorised_ports_client.update_ports_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Update nonexistent ports")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_nonexistent_port(self, ports_client: PortsClient):
        request = UpdatedPortSchema()
        response = ports_client.update_ports_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_update_nonexistent_port(response=response)



    @allure.title("[200]OK - Delete configured ports")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_port(self,
                         function_ports: PortsFixture,
                         ports_session: PortsSession):
        request = DeletePortsRequestSchema()
        response = ports_session.delete_ports_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Delete port by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_by_unauthorised_user(self, unauthorised_ports_session: PortsSession):
        request = DeletePortsRequestSchema()
        response = unauthorised_ports_session.delete_ports_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Delete port with incorrect body")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_port_with_incorrect_body(self, ports_session: PortsSession):
        response = ports_session.incorrect_delete_ports_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_delete_port_with_incorrect_body(response=response)




@pytest.mark.port_status
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.PORT_STATUS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.PORT_STATUS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.PORT_STATUS)
class TestPortStatus:

    @allure.title("[200]OK - Update port status")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_port_status(self, ports_client: PortsClient):
        request = UpdatePortStatusRequestSchema()
        response = ports_client.update_port_status_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Update port status by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_port_status_by_unauthorised_user(self, unauthorised_ports_client: PortsClient):
        request = UpdatePortStatusRequestSchema()
        response = unauthorised_ports_client.update_port_status_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Invalid update port status")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_invalid_update_port_status(self, ports_client: PortsClient):
        request = UpdatePortStatusRequestSchema(port="33/0",
                                                status=False)
        response = ports_client.update_port_status_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_invalid_update_port_status_response(response=response)




@pytest.mark.ports_all
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.PORTS_ALL)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.PORTS_ALL)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.PORTS_ALL)
class TestPortsAll:

    @allure.title("[200]OK - Get all ports list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_all_ports_list(self, ports_client: PortsClient):
        response = ports_client.get_all_ports_list_api()
        response_data = GetAllPortsListResponse.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get all ports list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_all_ports_list_by_unauthorised_user(self, unauthorised_ports_client: PortsClient):
        response = unauthorised_ports_client.get_all_ports_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())