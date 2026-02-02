import allure
from typing import Any
from requests import Session, Response


class APISession:
    def __init__(self, session: Session):
        """
        Базовый API клиент, принимающий объект httpx.Client.

        :param client: экземпляр httpx.Client для выполнения HTTP-запросов
        """
        self.session = session

    @allure.step('Make DELETE-request to {url}')
    def delete(self,
               url: str,
               json: Any | None = None,
               ) -> Response:
        """
        Выполняет DELETE-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные для удаления в формате JSON.
        :return: Объект requests.Response с данными ответа.
        """
        return self.session.delete(url=url,
                                   json=json)