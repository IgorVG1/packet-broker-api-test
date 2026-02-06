import allure, pytest

from http import HTTPStatus

from clients.analysis_ports.analysis_ports_client import AnalysisPortsClient, AnalysisPortsSession
from clients.analysis_ports.analysis_ports_schema import GetAnalysisPortsResponseSchema, \
    CreateAnalysisPortRequestSchema, UpdateAnalysisPortRequestSchema, DeleteAnalysisPortRequestSchema
from clients.errors_schema import AuthenticationErrorResponseSchema
from fixtures.analysis_ports import AnalysisPortsFixture
from tests.analysis_ports.analysis_ports_assertions import assert_create_analysis_port_response, \
    assert_create_already_creating_analysis_port_response, assert_update_analysis_port_response, \
    assert_update_nonexistent_analysis_port_response, assert_delete_nonexistent_analysis_port_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('ANALYSIS_PORTS')


@pytest.mark.analysis_ports
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.ANALYSIS_PORTS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.ANALYSIS_PORTS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.ANALYSIS_PORTS)
class TestAnalysisPorts:

    @allure.title("[200]OK - Get analysis port list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_analysis_port_list(self,
                                    function_analysis_port: AnalysisPortsFixture,
                                    analysis_ports_client: AnalysisPortsClient,
                                    function_analysis_port_tear_down):

        response = analysis_ports_client.get_analysis_port_list_api()
        response_data = GetAnalysisPortsResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get analysis port list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_analysis_port_list_by_unauthorised_user(self,
                                                         unauthorised_analysis_ports_client: AnalysisPortsClient):
        response = unauthorised_analysis_ports_client.get_analysis_port_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create analysis port")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_analysis_port(self,
                                  analysis_ports_client: AnalysisPortsClient,
                                  function_analysis_port_tear_down):

        request = CreateAnalysisPortRequestSchema()
        response = analysis_ports_client.create_analysis_port_api(request=request)

        response_get = analysis_ports_client.get_analysis_port_list_api()
        actual_analysis_port_list = GetAnalysisPortsResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_create_analysis_port_response(actual=actual_analysis_port_list,
                                             expected=request)


    @allure.title("[403]FORBIDDEN - Create analysis port by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_analysis_port_by_unauthorised_user(self,
                                                       unauthorised_analysis_ports_client: AnalysisPortsClient):
        request = CreateAnalysisPortRequestSchema()
        response = unauthorised_analysis_ports_client.create_analysis_port_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Create already creating analysis port")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_already_creating_analysis_port(self,
                                                   function_analysis_port: AnalysisPortsFixture,
                                                   analysis_ports_client: AnalysisPortsClient,
                                                   function_analysis_port_tear_down):

        request = CreateAnalysisPortRequestSchema()
        response = analysis_ports_client.create_analysis_port_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_create_already_creating_analysis_port_response(response=response)


    @allure.title("[200]OK - Update analysis port")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_analysis_port(self,
                                  function_analysis_port: AnalysisPortsFixture,
                                  analysis_ports_client: AnalysisPortsClient,
                                  function_analysis_port_tear_down):

        request = UpdateAnalysisPortRequestSchema()
        response = analysis_ports_client.update_analysis_port_api(request=request)

        response_get = analysis_ports_client.get_analysis_port_list_api()
        actual_analysis_port_list = GetAnalysisPortsResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_update_analysis_port_response(actual=actual_analysis_port_list,
                                             expected=request)

        request_tear_down = UpdateAnalysisPortRequestSchema(ports=['L1'])
        analysis_ports_client.update_analysis_port_api(request=request_tear_down)


    @allure.title("[403]FORBIDDEN - Update analysis port by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_analysis_port_by_unauthorised_user(self,
                                                       unauthorised_analysis_ports_client: AnalysisPortsClient):
        request = UpdateAnalysisPortRequestSchema()
        response = unauthorised_analysis_ports_client.update_analysis_port_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Update nonexistent analysis port ")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_nonexistent_analysis_port(self,
                                              function_analysis_port_set_up,
                                              analysis_ports_client: AnalysisPortsClient):
        request = UpdateAnalysisPortRequestSchema()
        response = analysis_ports_client.update_analysis_port_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_update_nonexistent_analysis_port_response(response=response)


    @allure.title("[200]OK - Delete analysis port")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_analysis_port(self,
                                  function_analysis_port: AnalysisPortsFixture,
                                  analysis_ports_client: AnalysisPortsClient,
                                  analysis_ports_session: AnalysisPortsSession):

        request = DeleteAnalysisPortRequestSchema()
        response = analysis_ports_session.delete_analysis_port_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        request_check_deleted = DeleteAnalysisPortRequestSchema()
        response_check_deleted = analysis_ports_session.delete_analysis_port_api(request=request_check_deleted)

        assert_status_code(actual=response_check_deleted.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_delete_nonexistent_analysis_port_response(response=response_check_deleted)


    @allure.title("[403]FORBIDDEN - Delete analysis port by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_analysis_port_by_unauthorised_user(self, unauthorised_analysis_ports_session: AnalysisPortsSession):

        request = DeleteAnalysisPortRequestSchema()
        response = unauthorised_analysis_ports_session.delete_analysis_port_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Delete nonexistent analysis port")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_nonexistent_analysis_port(self, analysis_ports_session: AnalysisPortsSession):

        request = DeleteAnalysisPortRequestSchema()
        response = analysis_ports_session.delete_analysis_port_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_delete_nonexistent_analysis_port_response(response=response)