import allure
from typing import Any
from requests import Session, Response


class APISession:
    def __init__(self, session: Session):
        """
        Базовая API сессия, принимающий объект requests.Session.

        :param session: экземпляр requests.Session для выполнения HTTP-запросов
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