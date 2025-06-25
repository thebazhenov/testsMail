import allure

from services import BaseApiClient
from requests import Response


class System(BaseApiClient):

    def __init__(self, base_url):
        super().__init__(base_url)
        self.configuration = {
            3025: "smtp",
            3110: "pop3",
            3143: "imap",
        }

    @allure.step("Проверить статус сервера через GET запрос на endpoint /api/service/readiness")
    def checks_greenmail_readiness(self) -> Response:
        """
        Проверка статуса сервера
        """
        return self._request(method="GET", endpoint="/api/service/readiness")

    @allure.step("Получить конфигурацию сервера через GET запрос на endpoint /api/configuration")
    def gets_current_greenmail_configuration(self) -> Response:
        """
        Получение конфигурации сервера
        """
        return self._request(method="GET", endpoint="/api/configuration")

    @allure.step("Перезапустить конфигурацию сервера через POST запрос на endpoint /api/service/reset")
    def restarts_using_current_configuration(self, **kwargs) -> Response:
        """
        Перезапуск конфигурации сервера
        :param data: json in body
        """
        return self._request(method="POST", endpoint="/api/service/reset", **kwargs)

    @allure.step("Удаление всех писем через POST запрос на endpoint /api/mail/purge")
    def purges_all_mails(self, data: dict = None) -> Response:
        """
        Удаление всех писем
        :param data: json in body
        """
        return self._request(method="POST", endpoint="/api/mail/purge", json=data)

    def check_data_configuration(self, models_list):
        for model in models_list:
            if model.port in self.configuration:
                assert self.configuration.get(model.port) == model.protocol, \
                    f"Протокол для порта {model.port} должен быть '{self.configuration[model.port]}', но получен '{model.protocol}'"
        return True

