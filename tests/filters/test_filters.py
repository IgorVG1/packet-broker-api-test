import allure, pytest

from http import HTTPStatus
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.filters.filters_client import FiltersClient, FiltersSession
from clients.filters.filters_schema import CreateFilterSchema
from config import settings
from fixtures.filters import FiltersFixture
from tests.filters.filters_data import FILTERS_FOR_DELETE
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger

logger = get_logger('FILTERS')


@pytest.mark.balancing
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.FILTERS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.FILTERS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.FILTERS)
class TestFilters:

    @allure.title("[200]OK - Get filters list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_filters_list(self, filters_client: FiltersClient):
        response = filters_client.get_filters_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Get filters list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_filters_list_by_unauthorised_user(self, unauthorised_filters_client: FiltersClient):
        response = unauthorised_filters_client.get_filters_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create filters")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_filters(self, filters_client: FiltersClient, function_filters_tear_down):
        request = CreateFilterSchema()
        response = filters_client.create_filters_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Create filters by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_filters_by_unauthorised_user(self, unauthorised_filters_client: FiltersClient):
        request = CreateFilterSchema()
        response = unauthorised_filters_client.create_filters_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Delete filters")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_filters(self, filters_session: FiltersSession, function_filters: FiltersFixture):
        request = FILTERS_FOR_DELETE.model_dump(by_alias=True)
        response = filters_session.delete_filters_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Delete filters by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_filters_by_unauthorised_user(self, unauthorised_filters_session: FiltersSession):
        request = FILTERS_FOR_DELETE.model_dump(by_alias=True)
        response = unauthorised_filters_session.delete_filters_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())