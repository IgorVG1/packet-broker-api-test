import allure, pytest

from http import HTTPStatus
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.ingress_groups.ingress_groups_client import IngressGroupsClient, IngressGroupsSession
from clients.ingress_groups.ingress_groups_schema import GetIngressGroupsResponseSchema, \
    CreateIngressGroupRequestSchema, UpdateIngressGroupRequestSchema, DeleteIngressGroupRequestSchema
from fixtures.ingress_groups import IngressGroupFixture
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


logger = get_logger('INGRESS_GROUPS')


@pytest.mark.ingress_groups
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.INGRESS_GROUPS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.INGRESS_GROUPS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.INGRESS_GROUPS)
class TestIngressGroups:

    @allure.title("[200]OK - Get ingress groups list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_ingress_group_list(self,
                                    function_ingress_groups_set_up,
                                    function_ingress_groups: IngressGroupFixture,
                                    ingress_groups_client: IngressGroupsClient,
                                    function_ingress_groups_tear_down):
        response = ingress_groups_client.get_ingress_group_list_api()
        response_data = GetIngressGroupsResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get ingress groups list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_ingress_group_list_by_unauthorised_user(self, unauthorised_ingress_groups_client: IngressGroupsClient):
        response = unauthorised_ingress_groups_client.get_ingress_group_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create ingress group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_ingress_group(self,
                                  function_ingress_groups_set_up,
                                  ingress_groups_client: IngressGroupsClient,
                                  function_ingress_groups_tear_down):
        request = CreateIngressGroupRequestSchema()
        response = ingress_groups_client.create_ingress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Create ingress group by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_ingress_group_by_unauthorised_user(self, unauthorised_ingress_groups_client: IngressGroupsClient):
        request = CreateIngressGroupRequestSchema()
        response = unauthorised_ingress_groups_client.create_ingress_group_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Create already creating ingress group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_already_creating_ingress_group(self,
                                                  function_ingress_groups_set_up,
                                                  function_ingress_groups: IngressGroupFixture,
                                                  ingress_groups_client: IngressGroupsClient,
                                                  function_ingress_groups_tear_down):
        request = CreateIngressGroupRequestSchema()
        response = ingress_groups_client.create_ingress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_create_already_creating_ingress_group_response(response=response)


    @allure.title("[200]OK - Update ingress group")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_ingress_group(self,
                                  function_ingress_groups_set_up,
                                  function_ingress_groups: IngressGroupFixture,
                                  ingress_groups_client: IngressGroupsClient,
                                  function_ingress_groups_tear_down):
        request = UpdateIngressGroupRequestSchema()
        response = ingress_groups_client.update_ingress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Update ingress group by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_ingress_group_by_unauthorised_user(self, unauthorised_ingress_groups_client: IngressGroupsClient):
        request = UpdateIngressGroupRequestSchema()
        response = unauthorised_ingress_groups_client.update_ingress_group_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Update nonexistent ingress group")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_nonexistent_ingress_group(self,
                                              function_ingress_groups_set_up,
                                              ingress_groups_client: IngressGroupsClient):
        request = UpdateIngressGroupRequestSchema()
        response = ingress_groups_client.update_ingress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_update_nonexistent_ingress_group_response(response=response)


    @allure.title("[200]OK - Delete ingress group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_ingress_group(self,
                                  function_ingress_groups_set_up,
                                  function_ingress_groups: IngressGroupFixture,
                                  ingress_groups_session: IngressGroupsSession):
        request = DeleteIngressGroupRequestSchema()
        response = ingress_groups_session.delete_ingress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Delete ingress group by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_ingress_group_by_unauthorised_user(self, unauthorised_ingress_groups_session: IngressGroupsSession):
        request = DeleteIngressGroupRequestSchema()
        response = unauthorised_ingress_groups_session.delete_ingress_group_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Delete nonexistent ingress group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_nonexistent_ingress_group(self,
                                              function_ingress_groups_set_up,
                                              ingress_groups_session: IngressGroupsSession):
        request = DeleteIngressGroupRequestSchema()
        response = ingress_groups_session.delete_ingress_group_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_delete_nonexistent_ingress_group_response(response=response)