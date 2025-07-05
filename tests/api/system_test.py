import allure
import pytest

from services import System, API_URL
from services.api.system.models import Message, CurrentConfiguration

@pytest.mark.api
@pytest.mark.full_regression
@allure.epic("System")
class TestSystem:

    @allure.title("Получение статуса сервера через POST запрос на endpoint /api/service/readiness")
    def test_check_greenmail_readiness(self, base_test):
        response = base_test.system.checks_greenmail_readiness()
        assert response.status_code == 200, response.status_code
        model = Message(**response.json())
        assert model.message == "Service running"

    @allure.title("Получение конфигурации сервера через POST запрос на endpoint /api/configuration")
    def test_current_greenmail_configuration(self, base_test):
        response = base_test.system.gets_current_greenmail_configuration()
        assert response.status_code == 200, response.status_code
        model = CurrentConfiguration(**response.json())
        configuration = {
            3025: "smtp",
            3110: "pop3",
            3143: "imap",
        }
        assert base_test.system.check_data_configuration(model.serverSetups, configuration=configuration)

    @allure.title("Применение конфигурации через POST запрос на endpoint /api/service/reset")
    def test_restart_greenmail_service(self, base_test):
        response = base_test.system.restarts_using_current_configuration()
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
    def test_restart_greenmail_service_negative(self, base_test, allure_title, data):
        allure.dynamic.title(allure_title)
        response = base_test.system.restarts_using_current_configuration(json=data)
        assert response.status_code == 200, response.status_code
        model = Message(**response.json())
        assert model.message == "Performed reset"

