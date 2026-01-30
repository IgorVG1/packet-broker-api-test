import allure, pytest

from http import HTTPStatus
from clients.balancing.balancing_client import BalancingClient, BalancingSession
from clients.balancing.balancing_schema import GetBalancingListResponseSchema, CreateBalancingRequestSchema, \
    UpdateBalancingRequestSchema, DeleteBalancingRequestSchema
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.public.public_client import PublicClient, PublicSession
from config import settings
from fixtures.balancing import BalancingFixture
from tests.balancing.balancing_assertions import assert_create_balancing_for_created_balancing_group_response, \
    assert_create_balancing_without_logic_id_response, assert_create_balancing_without_balance_type_response, \
    assert_update_balancing_without_logic_id_response, assert_update_balancing_without_balance_type_response, \
    assert_delete_had_been_deleted_balancing, assert_delete_without_logic_group_response
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.allure.severity import AllureSeverity
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger
from tools.assertions.errors import assert_error_for_not_authenticated_user


logger = get_logger('BALANCING')


@pytest.mark.balancing
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.BALANCING)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.BALANCING)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.BALANCING)
class TestBalancing:


    @allure.title("[200]OK - Get balancing list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_balancing_list(self, balancing_client: BalancingClient):
        response = balancing_client.get_balancing_list_api()
        response_data = GetBalancingListResponseSchema.model_validate_json(response.text)

        logger.info(f'Response data: \n{response.json()}')

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), response_data.model_json_schema())


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Get balancing list with access_token")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_get_balancing_list_without_access_token(self, public_client: PublicClient):
        response = public_client.get_balancing_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.title("[200]OK - Create balancing group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_balancing(self, balancing_client: BalancingClient, balancing_session: BalancingSession):
        try:
            request_delete = DeleteBalancingRequestSchema(logic_group=1)
            response_delete = balancing_session.delete_balancing_api(request=request_delete)

            logger.info(f'Delete balancing api response status code: "{response_delete.status_code}"')
            logger.info(f'Delete balancing api response body "{response_delete.text}"')
        finally:
            request = CreateBalancingRequestSchema()
            response = balancing_client.create_balancing_api(request=request)

            assert_status_code(response.status_code, HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Create balancing for created balancing group")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_create_balancing_for_created_balancing_group(self, balancing_client: BalancingClient):
        request = CreateBalancingRequestSchema()
        response = balancing_client.create_balancing_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)
        assert_create_balancing_for_created_balancing_group_response(response_str=response.text)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Create balancing without logicId")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_create_balancing_without_logic_id(self, balancing_client: BalancingClient):
        request = CreateBalancingRequestSchema(logic_id="")
        response = balancing_client.create_balancing_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)
        assert_create_balancing_without_logic_id_response(response_str=response.text)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Create balancing without balanceType")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_create_balancing_without_balance_type(self, balancing_client: BalancingClient):
        request = CreateBalancingRequestSchema(balance_type="")
        response = balancing_client.create_balancing_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)
        assert_create_balancing_without_balance_type_response(response_str=response.text)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Create balancing without access-token")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_create_balancing_without_access_token(self, public_client: PublicClient):
        request = CreateBalancingRequestSchema()
        response = public_client.create_balancing_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.title("[200]OK - Update balancing group")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_update_balancing(self, balancing_client: BalancingClient):
        request = UpdateBalancingRequestSchema()
        response = balancing_client.update_balancing_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.OK)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Update balancing group without logicId")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_update_balancing_without_logic_id(self, balancing_client: BalancingClient):
        request = UpdateBalancingRequestSchema(logic_id="")
        response = balancing_client.update_balancing_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)
        assert_update_balancing_without_logic_id_response(response_str=response.text)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Update balancing group without balanceType")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_update_balancing_without_balance_type(self, balancing_client: BalancingClient):
        request = UpdateBalancingRequestSchema(balance_type="")
        response = balancing_client.update_balancing_api(request=request)

        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)
        assert_update_balancing_without_balance_type_response(response_str=response.text)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Update balancing without access-token")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_update_balancing_without_access_token(self, public_client: PublicClient):
        request = UpdateBalancingRequestSchema()
        response = public_client.update_balancing_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.title("[200]OK - Delete balancing group")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_delete_balancing(self, balancing_session: BalancingSession, balancing_client: BalancingClient,function_balancing: BalancingFixture):
        request_delete = DeleteBalancingRequestSchema()
        response_delete = balancing_session.delete_balancing_api(request=request_delete)

        logger.info(f'Delete balancing api status code "{response_delete.status_code}"')
        logger.info(f'Delete balancing api response body "{response_delete.text}"')

        assert_status_code(response_delete.status_code, HTTPStatus.OK)

        request_create = CreateBalancingRequestSchema()
        response_create = balancing_client.create_balancing_api(request=request_create)

        logger.info(f'Create balancing api status code "{response_create.status_code}"')
        logger.info(f'Create balancing api response body "{response_create.text}"')


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @allure.title("[412]PRECONDITION_FAILED - Delete balancing group that had been deleted")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_delete_had_been_deleted_balancing(self, balancing_session: BalancingSession, function_balancing: BalancingFixture, function_balancing_after_delete):

        request = DeleteBalancingRequestSchema(logic_group=function_balancing.request.logic_id)
        balancing_session.delete_balancing_api(request=request)
        response = balancing_session.delete_balancing_api(request=request)

        assert_delete_had_been_deleted_balancing(response_str=response.text)
        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[412]PRECONDITION_FAILED - Delete balancing group without logicGroup")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_delete_without_logic_group(self, balancing_session: BalancingSession):

        request = DeleteBalancingRequestSchema(logic_group="")
        response = balancing_session.delete_balancing_api(request=request)

        assert_delete_without_logic_group_response(response_str=response.text)
        assert_status_code(response.status_code, HTTPStatus.PRECONDITION_FAILED)


    @pytest.mark.xdist_group(name=f"{settings.xdist_group_names.negative_tests}")
    @allure.title("[403]FORBIDDEN - Delete balancing without access-token")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MINOR)
    def test_delete_balancing_without_access_token(self, public_session: PublicSession):
        request = DeleteBalancingRequestSchema()
        response = public_session.delete_balancing_api(request=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())