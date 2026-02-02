import allure, pytest
from http import HTTPStatus
from clients.additional_filters.additional_filters_client import AdditionalFiltersClient, AdditionalFiltersSession
from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    CreateAdditionalFiltersSchema, UpdateAdditionalFiltersRequestSchema, DeleteAdditionalFiltersSchema, \
    DeleteAdditionalFiltersRequestSchema
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.public.public_client import PublicClient, PublicSession
from config import settings
from fixtures.additional_filters import AdditionalFilterFixture
from tests.additional_filters.additional_filters_assertions import \
    assert_create_additional_filters_without_direction_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.allure.severity import AllureSeverity
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger
from tools.assertions.errors import assert_error_for_not_authenticated_user


logger = get_logger('ADDITIONAL_FILTERS')


@pytest.mark.additional_filters
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.ADDITIONAL_FILTERS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.ADDITIONAL_FILTERS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.ADDITIONAL_FILTERS)
class TestAdditionalFilters:


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.additional_filters}")
    @allure.title("[200]OK - Create additional filters")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_additional_filters(self,additional_filters_client: AdditionalFiltersClient):
        request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema()])
        response = additional_filters_client.create_additional_filters_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Create additional filters without direction")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_additional_filters_without_direction(self,additional_filters_client: AdditionalFiltersClient):
        request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema(direction='')])
        response = additional_filters_client.create_additional_filters_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)
        assert_create_additional_filters_without_direction_response(response_str=response.text)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Create additional filters without access-token")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_additional_filters_without_access_token(self, public_client: PublicClient):
        request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema()])
        response = public_client.create_additional_filters_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.additional_filters}")
    @allure.title("[200]OK - Update additional filters")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_additional_filters(self, additional_filters_client: AdditionalFiltersClient):
            request = UpdateAdditionalFiltersRequestSchema()
            response = additional_filters_client.update_additional_filters_api(request=request)

            assert_status_code(response.status_code, HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Update additional filters without access-token")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_additional_filters_without_access_token(self, public_client: PublicClient):
        request = UpdateAdditionalFiltersRequestSchema()
        response = public_client.update_additional_filters_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.additional_filters}")
    @allure.title("[200]OK - Delete additional filters")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_additional_filters(self,
                                        additional_filters_session: AdditionalFiltersSession,
                                        function_additional_filters_for_delete: AdditionalFilterFixture):
        request = DeleteAdditionalFiltersRequestSchema([DeleteAdditionalFiltersSchema(value=function_additional_filters_for_delete.test_data.ip,
                                                 direction=function_additional_filters_for_delete.test_data.direction,
                                                 logicGroup=int(function_additional_filters_for_delete.test_data.group_id),
                                                 type=function_additional_filters_for_delete.test_data.type)])
        response = additional_filters_session.delete_additional_filters_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Delete additional filters without access-token")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_additional_filters_without_access_token(self, public_session: PublicSession,
                                        function_additional_filters_for_delete: AdditionalFilterFixture):
        request = DeleteAdditionalFiltersRequestSchema([DeleteAdditionalFiltersSchema()])
        response = public_session.delete_additional_filters_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())