import requests


class BaseApiClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, method, endpoint, **kwargs):
        """
        Метод для отправки api запросов
        :param method: Метод
        :param endpoint:
        :param kwargs:
        :return:
        """
        response = requests.request(method=method, url=f"{self.base_url}{endpoint}", **kwargs)

        return response
