import pytest
import allure

from conftest import USER_LOGIN, USER_PASSWORD, base_test, login_in_system
from services import MAIL_URL


@pytest.mark.ui
class TestLoginPage:

    @pytest.mark.critical
    def test_login(self, login_in_system, base_test):
        with allure.step(""):
            assert base_test.main_page.get_element(selector=base_test.main_page._username_locator).inner_text() == "test@localhost.com"

    @pytest.mark.parametrize(
        "login_in_system, allure_title, error_text",
        [
            ({"login": "t", "password": ""}, "Вход в систему", "text"),
            ({"login": "", "password": "password"}, "Вход в систему", "text"),
            ({"login": "", "password": ""}, "Вход в систему", "text"),
            ({"login": "user", "password": "user"}, "Вход в систему под несуществующим пользователем", "text")

        ],
        indirect=["login_in_system"]
    )
    def test_login_negative(self, login_in_system, allure_title, error_text):
        allure.dynamic.title(allure_title)
        with allure.step(""):
            pass

