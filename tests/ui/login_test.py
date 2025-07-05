import pytest
import allure

from conftest import USER_LOGIN, USER_PASSWORD, base_test, login_in_system
from services import MAIL_URL

@pytest.mark.full_regression
@pytest.mark.ui
@allure.epic("LoginPageUI")
class TestLoginPage:

    @pytest.mark.critical
    @allure.title("Авторизация на сайте")
    def test_login(self, login_in_system, base_test):
        with allure.step("Авторизоваться на сайте"):
            assert base_test.main_page.get_element(selector=base_test.main_page._username_locator).inner_text() == "test@localhost.com"

    @pytest.mark.parametrize(
        "login_in_system, allure_title",
        [
            ({"login": "t", "password": ""}, "Вход в систему с пустым паролем"),
            ({"login": "", "password": "password"}, "Вход в систему с пустым логином"),
            ({"login": "", "password": ""}, "Вход в систему с пустыми данными"),
            ({"login": "user", "password": "user"}, "Вход в систему под несуществующим пользователем")

        ],
        indirect=["login_in_system"]
    )
    def test_login_negative(self, base_test, login_in_system, allure_title):
        allure.dynamic.title(allure_title)
        with allure.step("Авторизоваться на сайте"):
            assert base_test.login_page.check_element_on_website(
                selector=base_test.login_page._login_form
            )
