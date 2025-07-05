import allure

from .base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._login_field = "//input[@name='_user']"
        self._password_field = "//input[@name='_pass']"
        self._sign_in_button = "//button[@type='submit']"
        self._login_form = "#login-form"

    @allure.step("Заполнение данных по авторизации, клик по кнопке авторизации")
    def login(self, email: str, password: str):
        """
        Заполняет поле логин, пароль, кликает по кнопке входа
        :param email: email пользователя
        :param password: пароль пользователя
        """
        self.typing(selector=self._login_field, text=email)
        self.typing(selector=self._password_field, text=password)
        # self.clickable(selector=self._sign_in_button)
        self.click(selector=self._sign_in_button)
