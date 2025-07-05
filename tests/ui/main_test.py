import allure
import pytest

from conftest import base_test, USER_LOGIN
from tests.api.user_test import send_letter_smtp

@pytest.mark.ui
@pytest.mark.full_regression
@allure.epic("MainPageUI")
class TestMainPage:

    @allure.title("Проверка окна входящие")
    def test_check_inbox(self, base_test, send_letter_smtp, login_in_system):
        letters = base_test.main_page.get_letters()
        assert len(letters) == 1
        letter_data = base_test.main_page.get_data_letter_short()
        assert letter_data.get("user_from") == USER_LOGIN
        assert letter_data.get("subject") == "test"

    @allure.title("Проверка переключения на отправленные письма")
    def test_switch_sentbox(self, base_test, login_in_system):
        base_test.main_page.switch_sendbox_page()
        assert "/?_task=mail&_mbox=Sent" in base_test.main_page.get_current_url

    @allure.title("Проверка переключения на контакты")
    @pytest.mark.critical
    def test_switch_contacts(self, base_test, login_in_system):
        base_test.main_page.switch_contacts_page()
        assert "?_task=addressbook" in base_test.main_page.get_current_url

    @allure.title("Проверка переключения на настройки")
    @pytest.mark.critical
    def test_switch_setting(self, base_test, login_in_system):
        base_test.main_page.switch_setting_page()
        assert "?_task=settings" in base_test.main_page.get_current_url
