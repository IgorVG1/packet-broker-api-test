import allure
from httpx import Response
from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.nodes.nodes_schema import CreateNodesRequestSchema
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.public_http_builder import get_public_http_client
from tools.routes import APIRoutes

# ----------------------------------------------------------------------------------------------------------------------

class NodesClient(APIClient):
    """
    Клиент для работы с /api/nodes/
    """
    @allure.step('Get nodes list')
    @tracker.track_coverage_httpx(f'{APIRoutes.NODES}')
    def get_nodes_list_api(self) -> Response:
        """
        Метод получения текущей конфигурации коммутатора на Web.
        При загрузке страницы http://192.168.7.57/configuration/.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.get(url=f'{APIRoutes.NODES}')


    @allure.step('Create nodes config')
    @tracker.track_coverage_httpx(f'{APIRoutes.NODES}')
    def create_nodes_api(self, request: CreateNodesRequestSchema) -> Response:
        """
        Метод сохранения текущей конфигурации c Web в базу данных.

        :param request: Словарь CreateNodesRequestSchema.model_dump(by_alias=True).
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.NODES}',
                         json=request.model_dump(by_alias=True))


    @allure.step('Create nodes config')
    @tracker.track_coverage_httpx(f'{APIRoutes.NODES}')
    def create_nodes_api_json(self, request_JSON: str) -> Response:
        """
        Метод сохранения текущей конфигурации c Web в базу данных.

        :param request_JSON: JSON-строка с тестовой node config.
        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.post(url=f'{APIRoutes.NODES}',
                         json=request_JSON)


    @allure.step('Apply nodes config')
    @tracker.track_coverage_httpx(f'{APIRoutes.NODES}')
    def apply_nodes_api(self) -> Response:
        """
        Метод применения текущей конфигурации Web.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.options(url=f'{APIRoutes.NODES}')


    @allure.step('Delete nodes config')
    @tracker.track_coverage_httpx(f'{APIRoutes.NODES}')
    def delete_nodes_api(self) -> Response:
        """
        Метод очистки текущей конфигурации Web из базы данных.

        :return: Ответ от сервера в виде объекта httpx.Response.
        """
        return self.delete(url=f'{APIRoutes.NODES}')

# ----------------------------------------------------------------------------------------------------------------------

def get_nodes_client(user: AuthenticationUserSchema) -> NodesClient:
    """
    Функция создаёт экземпляр NodesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию NodesClient.
    """
    return NodesClient(client=get_private_http_client(user=user))


def get_unauthorised_nodes_client() -> NodesClient:
    """
    Функция создаёт экземпляр неавторизованного NodesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию NodesClient без авторизации.
    """
    return NodesClient(client=get_public_http_client())