import allure, pytest

from http import HTTPStatus
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.selections.selections_client import SelectionsClient, SelectionsSession
from clients.selections.selections_schema import GetSelectionsResponseSchema, CreateSelectionRequestSchema, \
    DeleteSelectionRequestSchema
from fixtures.selections import SelectionFixture
from tests.selections.selections_assertions import check_get_selections_list_response, \
    check_create_selection_group_response, assert_create_already_creating_selection_group_response, \
    check_delete_selection_group_response, check_delete_selection_group_with_incorrect_body_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('SELECTIONS')


@pytest.mark.selections
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.SELECTIONS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.SELECTIONS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.SELECTIONS)
class TestSelections:

    @allure.title("[200]OK - Get selections list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_selections_list(self,
                                 function_selection: SelectionFixture,
                                 selections_client: SelectionsClient,
                                 function_selection_tear_down):

        response = selections_client.get_selections_list_api()
        response_data = GetSelectionsResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        check_get_selections_list_response(actual=response_data,
                                           expected=function_selection.request)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get selections list by unauthenticated user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_selections_list_by_unauthenticated_user(self, unauthorised_selections_client: SelectionsClient):

        response = unauthorised_selections_client.get_selections_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create selection group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_selection_group(self,
                                    function_selection_set_up,
                                    selections_client: SelectionsClient,
                                    function_selection_tear_down):

        request = CreateSelectionRequestSchema()
        response = selections_client.create_selection_api(request=request)

        response_get = selections_client.get_selections_list_api()
        actual_list_selections = GetSelectionsResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        check_create_selection_group_response(actual=actual_list_selections,
                                              expected=request)


    @allure.title("[403]FORBIDDEN - Create selection group by unauthenticated user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_selection_group_by_unauthenticated_user(self, unauthorised_selections_client: SelectionsClient):

        request = CreateSelectionRequestSchema()
        response = unauthorised_selections_client.create_selection_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Create already creating selection group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_already_creating_selection_group(self,
                                                     function_selection,
                                                     selections_client: SelectionsClient,
                                                     function_selection_tear_down):

        request = CreateSelectionRequestSchema()
        response = selections_client.create_selection_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_create_already_creating_selection_group_response(response=response)


    @allure.title("[200]OK - Delete selection group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_selection_group(self,
                                    function_selection,
                                    selections_client: SelectionsClient,
                                    selections_session: SelectionsSession):

        response_get_before = selections_client.get_selections_list_api()
        selections_list_before = GetSelectionsResponseSchema.model_validate_json(response_get_before.text)

        request = DeleteSelectionRequestSchema()
        response = selections_session.delete_selection_api(request=request)

        response_get_after = selections_client.get_selections_list_api()
        selections_list_after = GetSelectionsResponseSchema.model_validate_json(response_get_after.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        check_delete_selection_group_response(selections_list_before=selections_list_before,
                                              selections_list_after=selections_list_after)


    @allure.title("[403]FORBIDDEN - Delete selection group by unauthenticated user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_selection_group_by_unauthenticated_user(self,
                                                            unauthorised_selections_session: SelectionsSession):

        request = DeleteSelectionRequestSchema()
        response = unauthorised_selections_session.delete_selection_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Delete selection group with incorrect body")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_selection_group_with_incorrect_body(self, selections_session: SelectionsSession):

        request = DeleteSelectionRequestSchema(ingress_group="@")
        response = selections_session.delete_selection_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        check_delete_selection_group_with_incorrect_body_response(response=response)