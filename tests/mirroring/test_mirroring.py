import allure, pytest

from http import HTTPStatus

from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.mirroring.mirroring_client import MirroringClient, MirroringSession
from clients.mirroring.mirroring_schema import GetMirroringResponseSchema, UpdateMirroringRequestSchema, \
    DeleteMirroringRequestSchema, CreateMirroringRequestSchema
from config import settings
from fixtures.mirroring import MirroringFixture
from tests.mirroring.mirroring_assertions import assert_get_mirroring_list_response, assert_update_mirroring_response, \
    assert_delete_mirroring_response, assert_create_mirroring_response, \
    assert_create_already_creating_mirroring_group_response, assert_change_nonexistent_mirroring_group_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('MIRRORING')


@pytest.mark.mirroring
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.MIRRORING)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.MIRRORING)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.MIRRORING)
class TestMirroring:


    @allure.title("[200]OK - Get mirroring list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_mirroring_list(self,
                                function_mirroring: MirroringFixture,
                                mirroring_client: MirroringClient,
                                function_mirroring_tear_down):
        logger.info('[Set-up completed] : Mirroring group was created.')

        response = mirroring_client.get_mirroring_list_api()
        response_data = GetMirroringResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        assert_get_mirroring_list_response(response_get_mirroring=response_data.root[0],
                                           request_create_mirroring=function_mirroring.request)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Get mirroring list by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_mirroring_list_by_unauthorised_user(self,unauthorised_mirroring_client: MirroringClient):
        response = unauthorised_mirroring_client.get_mirroring_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())



    @allure.title("[200]OK - Create mirroring group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_mirroring(self,
                              function_mirroring_set_up,
                              mirroring_client: MirroringClient,
                              function_mirroring_tear_down):

        request = CreateMirroringRequestSchema()
        response_create = mirroring_client.create_mirroring_api(request=request)

        response_get = mirroring_client.get_mirroring_list_api()
        response_get_data = GetMirroringResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response_create.status_code,
                           expected=HTTPStatus.OK)
        assert_create_mirroring_response(actual=response_get_data.root[0],
                                         expected=request)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Create mirroring group by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_mirroring_list_by_unauthorised_user(self,unauthorised_mirroring_client: MirroringClient):
        request = CreateMirroringRequestSchema()
        response = unauthorised_mirroring_client.create_mirroring_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Create already creating mirroring group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST, AllureTag.FLAKY_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_already_creating_mirroring(self,
                              function_mirroring: MirroringFixture,
                              mirroring_client: MirroringClient,
                              function_mirroring_tear_down):
        logger.info('[Set-up completed] : Mirroring group was created.')

        request = CreateMirroringRequestSchema()
        response = mirroring_client.create_mirroring_api(request=request)
        response_text = response.text

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_create_already_creating_mirroring_group_response(response_text=response_text)



    @allure.title("[200]OK - Update mirroring group")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_update_mirroring(self,
                              function_mirroring: MirroringFixture,
                              mirroring_client: MirroringClient,
                              function_mirroring_tear_down):
        logger.info('[Set-up completed] : Mirroring group was created.')

        request_update = UpdateMirroringRequestSchema()
        response_update = mirroring_client.update_mirroring_api(request=request_update)

        response_get = mirroring_client.get_mirroring_list_api()
        response_get_data = GetMirroringResponseSchema.model_validate_json(response_get.text)

        assert_status_code(actual=response_update.status_code,
                           expected=HTTPStatus.OK)
        assert_update_mirroring_response(actual=response_get_data.root[0],
                                         expected=request_update)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Update mirroring group by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_mirroring_list_by_unauthorised_user(self,unauthorised_mirroring_client: MirroringClient):
        request = UpdateMirroringRequestSchema()
        response = unauthorised_mirroring_client.update_mirroring_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Update nonexistent mirroring group")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST, AllureTag.FLAKY_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_nonexistent_mirroring(self,
                                          mirroring_client: MirroringClient,
                                          mirroring_session: MirroringSession):
        try:
            request_delete = DeleteMirroringRequestSchema()
            mirroring_session.delete_mirroring_api(request=request_delete)
        finally:
            request = UpdateMirroringRequestSchema()
            response = mirroring_client.update_mirroring_api(request=request)
            response_text = response.text

            assert_status_code(actual=response.status_code,
                               expected=HTTPStatus.PRECONDITION_FAILED)
            assert_change_nonexistent_mirroring_group_response(response_text=response_text)



    @allure.title("[200]OK - Delete mirroring group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_mirroring(self,
                              mirroring_client: MirroringClient,
                              function_mirroring: MirroringFixture,
                              mirroring_session: MirroringSession):
        logger.info('[Set-up completed] : Mirroring group was created.')

        request_delete = DeleteMirroringRequestSchema()
        response_delete = mirroring_session.delete_mirroring_api(request=request_delete)

        logger.info('Mirroring group was deleted.')

        response_get = mirroring_client.get_mirroring_list_api()
        response_get_data = GetMirroringResponseSchema.model_validate_json(response_get.text)

        logger.info('Actual mirroring list was received.')

        assert_status_code(actual=response_delete.status_code,
                           expected=HTTPStatus.OK)
        assert_delete_mirroring_response(actual_mirroring_list=response_get_data.root)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Delete mirroring group by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_mirroring_list_by_unauthorised_user(self,unauthorised_mirroring_session: MirroringSession):
        request = DeleteMirroringRequestSchema()
        response = unauthorised_mirroring_session.delete_mirroring_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Delete nonexistent mirroring group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_nonexistent_mirroring(self, mirroring_session: MirroringSession):
        try:
            request_delete = DeleteMirroringRequestSchema()
            mirroring_session.delete_mirroring_api(request=request_delete)
        finally:
            request = DeleteMirroringRequestSchema()
            response = mirroring_session.delete_mirroring_api(request=request)
            response_text = response.text

            assert_status_code(actual=response.status_code,
                               expected=HTTPStatus.PRECONDITION_FAILED)
            assert_change_nonexistent_mirroring_group_response(response_text=response_text)