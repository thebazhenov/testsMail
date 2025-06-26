import allure

from services import BaseApiClient
from requests import Response


class System(BaseApiClient):

    @allure.step("Получить статус сервера через GET запрос на endpoint /api/service/readiness")
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

    @staticmethod
    def check_data_configuration(models_list, configuration: dict) -> bool:
        """
        Проверка конфигурации сервера
        :param configuration: Словарь, где ключ номер порта, а значение протокол
        :param models_list: CurrentConfiguration.serverSetups
        :return: Возвращает true в случае, если все совпало
        """
        if len(models_list) < 1:
            return False
        for model in models_list:
            if model.port in configuration:
                assert configuration.get(model.port) == model.protocol, \
                    f"Протокол для порта {model.port} должен быть '{configuration[model.port]}', но получен '{model.protocol}'"
        return True

