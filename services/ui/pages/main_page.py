import allure

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
        self._title_letter = ".rcmContactAddress"
        self._subject_letter = "//span[@class='subject']//span[text()]"
        self._sendbox_button = "//li[@id='rcmliU2VudA']//a"
        self._header_title = "#messagelist-header .header-title"
        self._write_letter_endpoint = "/?_task= mail & _action=compose"
        self._sendbox_endpoint = "/?_task=mail&_mbox=Sent"
        self._contacts_button = ".contacts"
        self._setting_button = ".settings"

    @allure.step("Открыть страницу отправки письма  по url")
    def open_window_letter(self):
        """
        Открывает страницу отправки письма
        :return:
        """
        self.open(url=f"{MAIL_URL}{self._write_letter_endpoint}")

    @allure.step("Открыть страницу входящих писем по url")
    def open_sendbox_page(self):
        """
        Открывает страницу входящих писем
        :return:
        """
        self.open(url=f"{MAIL_URL}{self._sendbox_endpoint}")

    @allure.step("Нажать на 'Контакты'")
    def switch_contacts_page(self):
        """
        Кликает по кнопке 'Контакты'
        :return:
        """
        self.page.wait_for_load_state(state="networkidle")
        self.click(selector=self._contacts_button)

    @allure.step("Нажать на 'Настройки'")
    def switch_setting_page(self):
        """
        Кликает по кнопке 'Настройки'
        :return:
        """
        self.page.wait_for_load_state(state="networkidle")
        self.click(selector=self._setting_button)

    @allure.step("Нажать на 'Отправленные'")
    def switch_sendbox_page(self) -> None:
        """
        Осуществляет переход путем нажатия на кнопку 'Отправленные'
        :return: None
        """
        self.page.wait_for_load_state(state="networkidle")
        self.click(selector=self._sendbox_button)

    def get_data_letter_short(self, index: int = 0) -> dict:
        """
        Возвращает короткую информацию по письму с вкладки
        :return: dict
        """
        element = self.get_letters()[index]
        title = element.locator(self._title_letter).inner_text()
        subject = element.locator(self._subject_letter).inner_text()
        return {
            "user_from": title,
            "subject": subject
        }

    def get_header_title(self):
        """
        Возвращает элемент активного box
        :return:
        """
        return self.get_element(selector=self._header_title)

    def get_letters(self):
        return self.get_element(selector=self._letters).all()
