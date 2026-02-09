import allure, pytest

from http import HTTPStatus
from clients.errors_schema import AuthenticationErrorResponseSchema
from clients.nodes.nodes_client import NodesClient
from clients.nodes.nodes_schema import CreateNodesRequestSchema
from tests.nodes.nodes_assertions import assert_apply_invalid_nodes_response
from tests.nodes.nodes_data import NODES_CONFIG_JSON
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.severity import AllureSeverity
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.errors import assert_error_for_not_authenticated_user
from tools.assertions.schema import validate_json_schema
from tools.logger import get_logger


logger = get_logger('NODES')


@pytest.mark.nodes
@pytest.mark.regression
@allure.tag(AllureTag.REGRESSION, AllureTag.NODES)
@allure.epic(AllureEpic.PACKET_BROKER)
@allure.feature(AllureFeature.NODES)
@allure.parent_suite(AllureEpic.PACKET_BROKER)
@allure.suite(AllureFeature.NODES)
class TestNodes:

    @allure.title("[200]OK - Get nodes list")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_get_nodes_list(self, nodes_client: NodesClient):
        response = nodes_client.get_nodes_list_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Get nodes list by unauthenticated user")
    @allure.tag(AllureTag.GET_ENTITIES, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_get_nodes_list_by_unauthenticated_user(self, unauthorised_nodes_client: NodesClient):
        response = unauthorised_nodes_client.get_nodes_list_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[200]OK - Create nodes config")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_create_nodes(self,
                          function_node_set_up,
                          nodes_client: NodesClient,
                          function_node_tear_down):
        request = NODES_CONFIG_JSON
        response = nodes_client.create_nodes_api_json(request_JSON=request)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)
        validate_json_schema(instance=request,
                             schema=CreateNodesRequestSchema.model_json_schema())


    @allure.title("[403]FORBIDDEN - Create nodes config by unauthenticated user")
    @allure.tag(AllureTag.CREATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_create_nodes_by_unauthenticated_user(self, unauthorised_nodes_client: NodesClient):
        request = NODES_CONFIG_JSON
        response = unauthorised_nodes_client.create_nodes_api_json(request_JSON=request)
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @pytest.mark.order(1)
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @allure.title("[200]OK - Apply nodes config")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.POSITIVE_TEST, AllureTag.FLAKY_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_apply_nodes(self,
                         function_nodes_return_config,
                         nodes_client: NodesClient):

        response = nodes_client.apply_nodes_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Apply nodes config by unauthenticated user")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_apply_nodes_by_unauthenticated_user(self, unauthorised_nodes_client: NodesClient):
        response = unauthorised_nodes_client.apply_nodes_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())


    @allure.title("[412]PRECONDITION_FAILED - Apply invalid nodes config")
    @allure.tag(AllureTag.UPDATE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_apply_invalid_nodes(self,
                                 function_node_set_up,
                                 nodes_client: NodesClient,
                                 function_node_tear_down):

        request_create = NODES_CONFIG_JSON
        nodes_client.create_nodes_api_json(request_JSON=request_create)

        response = nodes_client.apply_nodes_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.PRECONDITION_FAILED)
        assert_apply_invalid_nodes_response(response=response)


    @allure.title("[200]OK - Delete nodes config")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.POSITIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(AllureSeverity.BLOCKER)
    def test_delete_nodes(self,
                          nodes_client: NodesClient,
                          function_node_tear_down):

        response = nodes_client.delete_nodes_api()

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.OK)


    @allure.title("[403]FORBIDDEN - Delete nodes config by unauthenticated user")
    @allure.tag(AllureTag.DELETE_ENTITY, AllureTag.NEGATIVE_TEST)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(AllureSeverity.MAJOR)
    def test_delete_nodes_by_unauthenticated_user(self, unauthorised_nodes_client: NodesClient):
        response = unauthorised_nodes_client.delete_nodes_api()
        response_data = AuthenticationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code,
                           expected=HTTPStatus.FORBIDDEN)
        assert_error_for_not_authenticated_user(response=response_data)
        validate_json_schema(instance=response.json(),
                             schema=response_data.model_json_schema())