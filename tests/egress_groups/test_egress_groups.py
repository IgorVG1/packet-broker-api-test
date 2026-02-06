import allure, pytest

from http import HTTPStatus

from clients.egress_groups.egress_groups_client import EgressGroupsClient, EgressGroupsSession
from clients.egress_groups.egress_groups_schema import GetEgressGroupsResponseSchema, CreateEgressGroupRequestSchema, \
    UpdateEgressGroupRequestSchema, DeleteEgressGroupRequestSchema
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.ingress_groups.ingress_groups_client import IngressGroupsClient, IngressGroupsSession
from clients.ingress_groups.ingress_groups_schema import GetIngressGroupsResponseSchema, \
    CreateIngressGroupRequestSchema, UpdateIngressGroupRequestSchema, DeleteIngressGroupRequestSchema
from fixtures.egress_groups import EgressGroupFixture
from fixtures.ingress_groups import IngressGroupFixture
from tests.egress_groups.egress_groups_assertions import assert_create_egress_group_response, \
    assert_create_already_creating_egress_group_response, assert_update_egress_group_response, \
    assert_update_nonexistent_egress_group_response, assert_delete_nonexistent_egress_group_response
from tests.ingress_groups.ingress_groups_assertions import assert_create_already_creating_ingress_group_response, \
    assert_update_nonexistent_ingress_group_response, assert_delete_nonexistent_ingress_group_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('EGRESS_GROUPS')


@pytest.mark.egress_groups
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.EGRESS_GROUPS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.EGRESS_GROUPS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.EGRESS_GROUPS)
class TestEgressGroups:

    @allure.title("[200]OK - Get egress group list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_egress_group_list(self, egress_groups_client: EgressGroupsClient):
        response = egress_groups_client.get_egress_group_list_api()
        response_data = GetEgressGroupsResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get egress group list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_egress_group_list_by_unauthorised_user(self, unauthorised_egress_groups_client: EgressGroupsClient):
        response = unauthorised_egress_groups_client.get_egress_group_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create egress group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_egress_group(self,
                                 egress_groups_client: EgressGroupsClient,
                                 function_egress_group_tear_down):

        request = CreateEgressGroupRequestSchema()
        response = egress_groups_client.create_egress_group_api(request=request)

        response_get = egress_groups_client.get_egress_group_list_api()
        actual_egress_group_list = GetEgressGroupsResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        assert_create_egress_group_response(actual=actual_egress_group_list,
                                            expected=request)


    @allure.title("[403]FORBIDDEN - Create egress group by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_egress_group_by_unauthorised_user(self, unauthorised_egress_groups_client: EgressGroupsClient):
        request = CreateEgressGroupRequestSchema()
        response = unauthorised_egress_groups_client.create_egress_group_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Create already creating egress group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_already_creating_egress_group(self,
                                                  function_egress_group: EgressGroupFixture,
                                                  egress_groups_client: EgressGroupsClient,
                                                  function_egress_group_tear_down):

        request = CreateEgressGroupRequestSchema()
        response = egress_groups_client.create_egress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_create_already_creating_egress_group_response(response=response)


    @allure.title("[200]OK - Update egress group")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_egress_group(self,
                                 egress_groups_client: EgressGroupsClient,
                                 function_egress_group_return_config):

        request = UpdateEgressGroupRequestSchema()
        response = egress_groups_client.update_egress_group_api(request=request)

        response_get = egress_groups_client.get_egress_group_list_api()
        actual_egress_group_list = GetEgressGroupsResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_update_egress_group_response(actual=actual_egress_group_list,
                                            expected=request)


    @allure.title("[403]FORBIDDEN - Update egress group by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_egress_group_by_unauthorised_user(self, unauthorised_egress_groups_client: EgressGroupsClient):

        request = UpdateEgressGroupRequestSchema()
        response = unauthorised_egress_groups_client.update_egress_group_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Update nonexistent egress group")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_nonexistent_egress_group(self,
                                             egress_groups_client: EgressGroupsClient):

        request = UpdateEgressGroupRequestSchema(group_id='egress-9',
                                                 logic_group='selection-9')
        response = egress_groups_client.update_egress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_update_nonexistent_egress_group_response(response=response)


    @allure.title("[200]OK - Delete egress group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_egress_group(self,
                                 function_egress_group: EgressGroupFixture,
                                 egress_groups_session: EgressGroupsSession):

        request = DeleteEgressGroupRequestSchema()
        response = egress_groups_session.delete_egress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Delete egress group by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_egress_group_by_unauthorised_user(self, unauthorised_egress_groups_session: EgressGroupsSession):

        request = DeleteEgressGroupRequestSchema()
        response = unauthorised_egress_groups_session.delete_egress_group_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Delete nonexistent egress group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_nonexistent_egress_group(self,
                                             egress_groups_session: EgressGroupsSession):

        request = DeleteEgressGroupRequestSchema(group_id='egress-9',
                                                 logic_group='selection-9')
        response = egress_groups_session.delete_egress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_delete_nonexistent_egress_group_response(response=response)