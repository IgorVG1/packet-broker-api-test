import allure, pytest, time

from http import HTTPStatus
from clients.custom_config.custom_config_client import CustomConfigClient
from clients.custom_config.custom_config_schema import UploadCustomConfigRequestSchema
from clients.errors_schema import AuthenticationErrorResponseSchema
from config import settings
from tests.custom_config.custom_config_assertions import assert_download_custom_config_response,\
    assert_upload_broken_custom_config
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.allure.severity import AllureSeverity
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger
from tools.assertions.errors import assert_error_for_not_authenticated_user


logger = get_logger('CUSTOM_CONFIG')


@pytest.mark.custom_config
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.CUSTOM_CONFIG)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.CUSTOM_CONFIG)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.CUSTOM_CONFIG)
class TestCustomConfig:


    @allure.title("[200]OK - Download custom config from switch")
    @allure.tag(AllureTag.GET_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_download_custom_config(self, custom_config_client: CustomConfigClient, function_custom_config_tear_down):
        response = custom_config_client.download_custom_config_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        assert_download_custom_config_response(response=response)

        logger.info(f'Response content-type: "{type(response.content)}".')
        logger.info(f'Size of download content: "{response.num_bytes_downloaded} bytes".')


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Download custom config from switch by unauthorised user")
    @allure.tag(AllureTag.GET_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_download_custom_config_by_unauthorised_user(self, unauthorised_custom_config_client: CustomConfigClient):
        response = unauthorised_custom_config_client.download_custom_config_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())



    @pytest.mark.order("last")
    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @allure.title("[200]OK - Upload my custom config to the switch")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST, AllureTag.FLAKY_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_upload_custom_config(self, custom_config_client: CustomConfigClient):
        request = UploadCustomConfigRequestSchema()

        start_upload_time = time.perf_counter()
        response = custom_config_client.upload_custom_config_api(request=request)
        end_upload_time = time.perf_counter()

        uploading_time = end_upload_time - start_upload_time
        logger.info(f'Time spent uploading user custom config to the switch: <{uploading_time:.3f} seconds.>')

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Upload my custom config to the switch by unauthorised user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_upload_custom_config_by_unauthorised_user(self, unauthorised_custom_config_client: CustomConfigClient):
        request = UploadCustomConfigRequestSchema()
        response = unauthorised_custom_config_client.upload_custom_config_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    # @pytest.mark.skip(reason='Тест ломает коммутатор')
    @pytest.mark.order("second_to_last")
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @allure.title('[412]PRECONDITION_FAILED - Upload my "broken" custom config to the switch')
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST, AllureTag.FLAKY_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_upload_broken_custom_config(self, custom_config_client: CustomConfigClient, function_custom_config_tear_down):
        request = UploadCustomConfigRequestSchema(config=settings.test_data.invalid_custom_config_json_file)
        response = custom_config_client.upload_custom_config_api(request=request)
        response_text = response.text

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_upload_broken_custom_config(response_text=response_text)



    @allure.title("[200]OK - Saving actual custom config")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_saving_custom_config(self, custom_config_client: CustomConfigClient, function_custom_config_tear_down):
        response = custom_config_client.saving_custom_config_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Saving actual custom config by unauthorised user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_saving_custom_config_by_unauthorised_user(self, unauthorised_custom_config_client: CustomConfigClient):
        response = unauthorised_custom_config_client.saving_custom_config_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())



    @allure.title("[200]OK - Restore saved custom config")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_restore_custom_config(self, custom_config_client: CustomConfigClient, function_custom_config_tear_down):
        response = custom_config_client.restore_custom_config_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Restore saved custom config by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_restore_custom_config_by_unauthorised_user(self, unauthorised_custom_config_client: CustomConfigClient):
        response = unauthorised_custom_config_client.restore_custom_config_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())



    @allure.title("[200]OK - Return default config")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_return_default_config(self,
                                   custom_config_client: CustomConfigClient,
                                   function_custom_config_tear_down):
        response = custom_config_client.return_default_config()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)



    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Return default config by unauthorised user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_return_default_config_by_unauthorised_user(self, unauthorised_custom_config_client: CustomConfigClient):
        response = unauthorised_custom_config_client.return_default_config()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())