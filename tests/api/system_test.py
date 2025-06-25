import allure
import pytest

from services import System, API_URL
from services.api.system.models import Message, CurrentConfiguration

@pytest.mark.api
@allure.epic("System")
class TestSystem:

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(cls):
        cls.system_api = System(base_url=API_URL)


    @allure.title("Проверка статуса сервера через POST запрос на endpoint /api/service/readiness")
    def test_check_greenmail_readiness(self):
        response = self.system_api.checks_greenmail_readiness()
        assert response.status_code == 200, response.status_code
        model = Message(**response.json())
        assert model.message == "Service running"

    @allure.title("Получение конфигурации сервера через POST запрос на endpoint /api/configuration")
    def test_current_greenmail_configuration(self):
        response = self.system_api.gets_current_greenmail_configuration()
        assert response.status_code == 200, response.status_code
        model = CurrentConfiguration(**response.json())
        assert self.system_api.check_data_configuration(model.serverSetups)

    @allure.title("Применение конфигурации через POST запрос на endpoint /api/service/reset")
    def test_restart_greenmail_service(self):
        response = self.system_api.restarts_using_current_configuration()
        assert response.status_code == 200, response.status_code
        model = Message(**response.json())
        assert model.message == "Performed reset"

    @pytest.mark.parametrize(
        "allure_title, data",
        [
            ("Негативный тест. Применение конфигурации через POST запрос на на endpoint /api/service/reset с json {{name: str}}"
             ,{"name": "str"}),

            ("Негативный тест. Применение конфигурации через POST запрос на на endpoint /api/service/reset с пустым json",{})
        ]
    )
    @pytest.mark.negative
    def test_restart_greenmail_service_negative(self, allure_title, data):
        allure.dynamic.title(allure_title)
        response = self.system_api.restarts_using_current_configuration(json=data)
        assert response.status_code == 200, response.status_code
        model = Message(**response.json())
        assert model.message == "Performed reset"

