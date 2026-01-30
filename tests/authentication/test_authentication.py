import allure, pytest

from http import HTTPStatus
from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import LoginRequestSchema,InvalidLoginResponseSchema
from config import settings
from tests.authentication.authentication_assertions import assert_invalid_log_in_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.allure.severity import AllureSeverity


@pytest.mark.authentication
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.AUTHENTICATION)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAdditionalFilters:


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Log in with invalid username")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_invalid_log_in(self, authentication_client: AuthenticationClient):
        request = LoginRequestSchema(username="username")
        response = authentication_client.login_api(request=request)
        response_data = InvalidLoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_invalid_log_in_response(response=response_data)