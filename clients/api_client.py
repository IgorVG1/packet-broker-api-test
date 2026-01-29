import allure
from typing import Optional, Any

from httpx import Client, URL, Response, QueryParams
from httpx._types import RequestData, RequestFiles


class APIClient:
    def __init__(self, client: Client):
        """
        Базовый API клиент, принимающий объект httpx.Client.

        :param client: экземпляр httpx.Client для выполнения HTTP-запросов
        """
        self.client = client

    @allure.step('Make GET-request to {url}')
    def get(self,
            url: str | URL,
            params: Optional[QueryParams] = None
            ) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL-адрес эндпоинта.
        :param params: GET-параметры запроса (например, ?key=value).
        :return: Объект Response с данными ответа.
        """
        return self.client.get(url=url,
                               params=params)

    @allure.step('Make POST-request to {url}')
    def post(self,
             url: str | URL,
             json: Optional[Any] = None,
             data: Optional[RequestData] = None,
             files: Optional[RequestFiles] = None
             ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :param data: Форматированные данные формы (например, application/x-www-form-urlencoded).
        :param files: Файлы для загрузки на сервер.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url=url,
                                json=json,
                                data=data,
                                files=files)

    @allure.step('Make PUT-request to {url}')
    def put(self,
            url: str | URL,
            json: Optional[Any] = None
            ) -> Response:
        """
        Выполняет PUT-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные для обновления в формате JSON.
        :return: Объект Response с данными ответа.
        """
        return self.client.put(url=url,
                               json=json)

    @allure.step('Make DELETE-request to {url}')
    def delete(self,
               url: str | URL
               ) -> Response:
        """
        Выполняет DELETE-запрос.

        :param url: URL-адрес эндпоинта.
        :return: Объект Response с данными ответа.
        """
        return self.client.delete(url=url)