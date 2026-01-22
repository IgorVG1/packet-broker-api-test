import allure, pytest
from http import HTTPStatus

import requests

from clients.additional_filters.additional_filters_client import get_additional_filters_client, AdditionalFiltersClient
from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    CreateAdditionalFiltersSchema, UpdateAdditionalFiltersRequestSchema, CreateAdditionalFiltersResponseSchema
from clients.authentication_client.authentication_client import get_authentication_client, AuthenticationClient
from clients.authentication_client.authentication_schema import LoginRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from fixtures.additional_filters import AdditionalFilterFixture
from fixtures.authentication import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.allure.severity import AllureSeverity


@pytest.mark.additional_filters
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.ADDITIONAL_FILTERS)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.ADDITIONAL_FILTERS)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.ADDITIONAL_FILTERS)
class TestAdditionalFilters:


    @allure.title("Create additional filters")
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_additional_filters(self, additional_filters_client: AdditionalFiltersClient):
        request = CreateAdditionalFiltersRequestSchema([CreateAdditionalFiltersSchema()])
        response = additional_filters_client.create_additional_filters_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.OK)


    @allure.title("Update additional filters")
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_additional_filters(self, additional_filters_client: AdditionalFiltersClient):
        request = UpdateAdditionalFiltersRequestSchema()
        response = additional_filters_client.update_additional_filters_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.OK)


    @allure.title("Delete additional filters")
    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_delete_additional_filters(self, function_user: UserFixture, function_additional_filters_for_delete: AdditionalFilterFixture):
        response = requests.delete(url='http://192.168.7.57/api/additional_filters/',
                                                             headers={
                                                                 "Authorization": f"Bearer {function_user.response.access}"},
                                                             json=[
                                                                 {
                                                                     "direction": "Src+Dst",
                                                                     "logicGroup": 1,
                                                                     "value": "1.1.1.1",
                                                                     "type": "pass"
                                                                 }
                                                             ])
        assert_status_code(response.status_code, HTTPStatus.OK)