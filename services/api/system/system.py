from services import BaseApiClient
from requests import Response


class System(BaseApiClient):

    def checks_greenmail_readiness(self) -> Response:
        """
        Проверка статуса сервера
        """
        return self._request(method="GET", endpoint="/api/service/readiness")

    def gets_current_greenmail_configuration(self) -> Response:
        """
        Получение конфигурации сервера
        """
        return self._request(method="GET", endpoint="/api/configuration")

    def restarts_using_current_configuration(self, data: dict = None) -> Response:
        """
        Перезапуск конфигурации сервера
        :param data: json in body
        """
        return self._request(method="POST", endpoint="/api/service/reset", json=data)

    def purges_all_mails(self, data: dict = None) -> Response:
        """
        Удаление всех писем
        :param data: json in body
        """
        return self._request(method="POST", endpoint="/api/mail/purge", json=data)
