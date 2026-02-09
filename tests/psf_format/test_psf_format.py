import allure, pytest

from http import HTTPStatus
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.psf_format.psf_format_client import PsfFormatClient, PsfFormatSession
from clients.psf_format.psf_format_schema import GetPsfFormatResponseSchema, CreatePsfFormatRequestSchema, \
    UpdatePsfFormatRequestSchema, DeletePsfFormatRequestSchema, GetPsfDmacResponseSchema, CreatePsfDmacRequestSchema
from fixtures.psf_format import PsfDmacFixture
from tests.psf_format.psf_format_assertions import assert_create_psf_format_response, \
    assert_create_already_creating_psf_format_response, assert_update_psf_format_response, \
    assert_update_nonexistent_psf_format_response, assert_create_psf_dmac_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('PSF_FORMAT')


@pytest.mark.psf_format
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.PSF_FORMAT)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.PSF_FORMAT)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.PSF_FORMAT)
class TestPsfFormat:

    @allure.title("[200]OK - Get psf format list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_psf_format_list(self,
                                 function_psf_format,
                                 psf_format_client: PsfFormatClient,
                                 function_psf_format_tear_down):

        response = psf_format_client.get_psf_format_list_api()
        response_data = GetPsfFormatResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get psf format list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_psf_format_list_by_unauthorised_user(self, unauthorised_psf_format_client: PsfFormatClient):

        response = unauthorised_psf_format_client.get_psf_format_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create psf format")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_psf_format(self,
                               psf_format_client: PsfFormatClient,
                               function_psf_format_tear_down):

        request = CreatePsfFormatRequestSchema()
        response = psf_format_client.create_psf_format_api(request=request)

        response_get = psf_format_client.get_psf_format_list_api()
        actual_psf_format_list = GetPsfFormatResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_create_psf_format_response(actual=actual_psf_format_list,
                                          expected=request)


    @allure.title("[403]FORBIDDEN - Create psf format by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_psf_format_by_unauthorised_user(self, unauthorised_psf_format_client: PsfFormatClient):
        request = CreatePsfFormatRequestSchema()
        response = unauthorised_psf_format_client.create_psf_format_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Create already creating psf format")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_already_creating_psf_format(self,
                                                function_psf_format,
                                                psf_format_client,
                                                function_psf_format_tear_down):

        request = CreatePsfFormatRequestSchema()
        response = psf_format_client.create_psf_format_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_create_already_creating_psf_format_response(response=response)


    @allure.title("[200]OK - Update psf format")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_psf_format(self,
                               function_psf_format,
                               psf_format_client,
                               function_psf_format_tear_down):

        request = UpdatePsfFormatRequestSchema()
        response = psf_format_client.update_psf_format_api(request=request)

        response_get = psf_format_client.get_psf_format_list_api()
        actual_psf_format_list = GetPsfFormatResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_update_psf_format_response(actual=actual_psf_format_list,
                                          expected=request)

        request_tear_down = UpdatePsfFormatRequestSchema(dmac='112233445566')
        psf_format_client.update_psf_format_api(request=request_tear_down)


    @allure.title("[403]FORBIDDEN - Update psf format by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_psf_format_by_unauthorised_user(self, unauthorised_psf_format_client: PsfFormatClient):
        request = UpdatePsfFormatRequestSchema()
        response = unauthorised_psf_format_client.update_psf_format_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Update nonexistent psf format ")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_nonexistent_psf_format(self,
                                           function_psf_format_set_up,
                                           psf_format_client: PsfFormatClient):
        request = UpdatePsfFormatRequestSchema()
        response = psf_format_client.update_psf_format_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)

        assert_update_nonexistent_psf_format_response(response=response)


    @allure.title("[200]OK - Delete psf format")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_psf_format(self,
                               function_psf_format,
                               psf_format_session: PsfFormatSession):

        request = DeletePsfFormatRequestSchema()
        response = psf_format_session.delete_psf_format_api(request=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Delete psf format by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_psf_format_by_unauthorised_user(self, unauthorised_psf_format_session: PsfFormatSession):

        request = DeletePsfFormatRequestSchema()
        response = unauthorised_psf_format_session.delete_psf_format_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())

#-----------------------------------------------------------------------------------------------------------------------

@pytest.mark.psf_dmac
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.PSF_DMAC)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.PSF_DMAC)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.PSF_DMAC)
class TestPsfDmac:

    @allure.title("[200]OK - Get psf dmac")
    @allure.tag(AllureTag.GET_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_psf_dmac(self,
                          function_psf_dmac: PsfDmacFixture,
                          psf_format_client: PsfFormatClient,
                          function_psf_dmac_tear_down):

        response = psf_format_client.get_psf_dmac_api()
        response_data = GetPsfDmacResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[403]FORBIDDEN - Get psf dmac by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_psf_dmac_by_unauthorised_user(self, unauthorised_psf_format_client: PsfFormatClient):

        response = unauthorised_psf_format_client.get_psf_dmac_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create psf dmac")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_psf_dmac(self,
                             psf_format_client: PsfFormatClient,
                             function_psf_dmac_tear_down):

        request = CreatePsfDmacRequestSchema()
        response = psf_format_client.create_psf_dmac_api(request=request)

        response_get = psf_format_client.get_psf_dmac_api()
        actual_psf_dmac = GetPsfDmacResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)

        assert_create_psf_dmac_response(actual=actual_psf_dmac,
                                        expected=request)


    @allure.title("[403]FORBIDDEN - Create psf dmac by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_psf_dmac_by_unauthorised_user(self, unauthorised_psf_format_client: PsfFormatClient):
        request = CreatePsfDmacRequestSchema()
        response = unauthorised_psf_format_client.create_psf_dmac_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)

        assert_error_for_not_authenticated_user(response=response_data)

        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())