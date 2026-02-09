import allure, pytest

from http import HTTPStatus
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.mirror_filter.mirror_filter_client import MirrorFilterClient, MirrorFilterSession
from clients.mirror_filter.mirror_filter_schema import GetMirrorFilterListResponseSchema, \
    CreateMirrorFilterRequestSchema, DeleteMirrorFilterRequestSchema, GetPsfMirrorFilterListResponseSchema
from tests.mirror_filter.mirror_filter_assertions import assert_create_mirror_filter_response, \
    assert_delete_nonexistent_mirror_filter_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('MIRROR_FILTER')


@pytest.mark.mirror_filter
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.MIRROR_FILTER)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.MIRROR_FILTER)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.MIRROR_FILTER)
class TestMirrorFilter:

    @allure.title("[200]OK - Get mirror filter list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_mirror_filter_list(self,
                                    function_mirror_filter_set_up,
                                    mirror_filter_client: MirrorFilterClient):
        response = mirror_filter_client.get_mirror_filter_list()
        response_data = GetMirrorFilterListResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get mirror filter list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_mirror_filter_list_by_unauthorised_user(self, unauthorized_mirror_filter_client: MirrorFilterClient):

        response = unauthorized_mirror_filter_client.get_mirror_filter_list()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create mirror filter")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_mirror_filter(self,
                                  mirror_filter_client: MirrorFilterClient,
                                  function_mirror_filter_tear_down):

        request = CreateMirrorFilterRequestSchema()
        response = mirror_filter_client.create_mirror_filter_api(request=request)

        response_get = mirror_filter_client.get_mirror_filter_list()
        actual_mirror_filter_list = GetMirrorFilterListResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_create_mirror_filter_response(actual=actual_mirror_filter_list,
                                             expected=request)


    @allure.title("[403]OK - Create mirror filter by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_mirror_filter_by_unauthorised_user(self, unauthorized_mirror_filter_client: MirrorFilterClient):

        request = CreateMirrorFilterRequestSchema()
        response = unauthorized_mirror_filter_client.create_mirror_filter_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Delete mirror filter")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_mirror_filter(self,
                                  function_mirror_filter,
                                  mirror_filter_session: MirrorFilterSession):

        request = DeleteMirrorFilterRequestSchema()
        response = mirror_filter_session.delete_mirror_filters(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        response_check_delete = mirror_filter_session.delete_mirror_filters(request=request)

        assert_delete_nonexistent_mirror_filter_response(response=response_check_delete)


    @allure.title("[403]OK - Delete mirror filter by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_mirror_filter_by_unauthorised_user(self, unauthorized_mirror_filter_session: MirrorFilterSession):

        request = DeleteMirrorFilterRequestSchema()
        response = unauthorized_mirror_filter_session.delete_mirror_filters(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Delete nonexistent mirror filter")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_nonexistent_mirror_filter(self, mirror_filter_session: MirrorFilterSession):

        request = DeleteMirrorFilterRequestSchema()
        response = mirror_filter_session.delete_mirror_filters(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_delete_nonexistent_mirror_filter_response(response=response)

#-----------------------------------------------------------------------------------------------------------------------

@pytest.mark.psf_mirror_filter
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.PSF_MIRROR_FILTER)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.PSF_MIRROR_FILTER)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.PSF_MIRROR_FILTER)
class TestPsfMirrorFilter:

    @allure.title("[200]OK - Get psf mirror filter")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_psf_mirror_filter_list(self,
                                        function_mirror_filter,
                                        mirror_filter_client: MirrorFilterClient):
        response = mirror_filter_client.get_psf_mirror_filter_list_api()
        response_data = GetPsfMirrorFilterListResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get psf mirror filter list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_psf_mirror_filter_list_by_unauthorised_user(self, unauthorized_mirror_filter_client: MirrorFilterClient):

        response = unauthorized_mirror_filter_client.get_psf_mirror_filter_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())