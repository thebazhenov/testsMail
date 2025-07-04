from services.ui.pages.base_page import BasePage
from playwright.sync_api import Page
from services import MAIL_URL

class MainPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._inbox_locator = "//span[@class='header-title' and text()='Входящие']"
        self._username_locator= "//span[@class='header-title username']"
        self._write_letter_button = "//a[@class='compose']"
        self._letters = ".message"

    def open_window_letter(self):
        self.open(url=f"{MAIL_URL}/?_task= mail & _action=compose")

    def get_letters(self):
        print(self.get_element(selector=self._letters))
        return self.get_element(selector=self._letters)


