import allure
from httpx import Response
from clients.additional_filters.additional_filters_schema import CreateAdditionalFiltersRequestSchema, \
    UpdateAdditionalFiltersRequestSchema, DeleteAdditionalFiltersRequestSchema
from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from tools.routes import APIRoutes


class AdditionalFiltersClient(APIClient):
    """
    Клиент для работы с /api/additional_filters/
    """
    @allure.step('Create additional filters')
    def create_additional_filters_api(self, request: CreateAdditionalFiltersRequestSchema) -> Response:
        """
        Метод создает дополнительные фильтры.

        :param request: Список словарей с direction, group_id(groupId), ip, type.
        :return: Ответ от сервера.
        """
        json_data = request.model_dump(by_alias=True)
        return self.post(url=f'{APIRoutes.ADDITIONAL_FILTERS}',
                         json=json_data)


    @allure.step('Update additional filters')
    def update_additional_filters_api(self, request: UpdateAdditionalFiltersRequestSchema) -> Response:
        """
        Метод сохраняет дополнительный фильтр.

        :param request: Список словарей с logic_id(logicId), filter_ip_white_enable(filterIPWhiteEnable), filter_ip_black_enable(filterIPBlackEnable).
        :return: Ответ от сервера.
        """
        return self.put(url=f'{APIRoutes.ADDITIONAL_FILTERS}',
                        json=request.model_dump(by_alias=True))


    @allure.step('Delete additional filters')
    def delete_additional_filters_api(self, request: DeleteAdditionalFiltersRequestSchema) -> Response:
        """
        Метод удаляет дополнительные фильтры.

        :param request: Список словарей с direction, logic_group(logicGroup), value, type.
        :return: Ответ от сервера.
        """
        return self.delete(url=f'{APIRoutes.ADDITIONAL_FILTERS}',
                           json_data=request.model_dump(by_alias=True))


def get_additional_filters_client(user: AuthenticationUserSchema) -> AdditionalFiltersClient:
    """
    Функция создаёт экземпляр AdditionalFiltersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AdditionalFiltersClient.
    """
    return AdditionalFiltersClient(client=get_private_http_client(user=user))