from select import select

from .base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._login_field = "//input[@name='_user']"
        self._password_field = "//input[@name='_pass']"
        self._sign_in_button = "//button[@type='submit']"

    def login(self, email: str, password: str):
        self.typing(selector=self._login_field, text=email)
        self.typing(selector=self._password_field, text=password)
        # self.clickable(selector=self._sign_in_button)
        self.click(selector=self._sign_in_button)


