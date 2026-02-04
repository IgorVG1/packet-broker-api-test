from typing import Any

import pytest
from pydantic import BaseModel

from clients.custom_config.custom_config_client import CustomConfigClient
from clients.custom_config.custom_config_schema import UploadCustomConfigRequestSchema
from clients.ingress_groups.ingress_groups_client import IngressGroupsClient, IngressGroupsSession, \
    get_ingress_group_client, get_unauthorised_ingress_group_client, get_ingress_group_session, \
    get_unauthorised_ingress_group_session
from clients.ingress_groups.ingress_groups_schema import CreateIngressGroupRequestSchema, \
    DeleteIngressGroupRequestSchema
from clients.nodes.nodes_client import NodesClient, get_nodes_client, get_unauthorised_nodes_client
from clients.nodes.nodes_schema import CreateNodesRequestSchema
from fixtures.authentication import UserFixture
from tests.nodes.nodes_data import NODES_CONFIG_JSON
from tools.logger import get_logger


logger = get_logger('NODES_FIXTURE')


@pytest.fixture(scope='function')
def nodes_client(function_user: UserFixture) -> NodesClient:
    return get_nodes_client(user=function_user.authentication_user)

@pytest.fixture(scope='function')
def unauthorised_nodes_client(function_user: UserFixture) -> NodesClient:
    return get_unauthorised_nodes_client()


@pytest.fixture(scope='function')
def function_node_set_up(nodes_client: NodesClient):
    """
    Фикстура для удаления текущей конфигурации на Web перед запуском теста.

    :param nodes_client: Фикстура с подготовленным клиентом для работы с /api/nodes/.
    """
    nodes_client.delete_nodes_api()

    logger.info('[Set-up completed] : Existed nodes config was deleted.')


@pytest.fixture(scope='function')
def function_node_tear_down(custom_config_client: CustomConfigClient):
    """
    Фикстура для удаления созданной входной группы по окончании теста.

    :param custom_config_client: Фикстура для возврата тестовой конфигурации коммутатора.
    """
    yield
    request = UploadCustomConfigRequestSchema()
    custom_config_client.upload_custom_config_api(request=request)

    logger.info('[Tear-down completed] : Test custom config was returned.')