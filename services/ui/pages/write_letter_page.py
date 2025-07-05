import allure

from services.ui.pages.base_page import BasePage
from playwright.sync_api import Page


class WriteLetterPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page=page)
        self._whoam_field = "//div[@id='compose_to']//input"
        self._topic_field = "//div[@id='compose_subject']//input"
        self._message_field = "//textarea[@name='_message']"
        self._send_message_button = "//button[@class='btn btn-primary send']"
        self._label = lambda text: f"//div[@id='messagestack']//span[contains(text(), '{text}')]"

    @allure.step("Ввести email в поле 'Кому'")
    def typing_whoam(self, whoam: str) -> None:
        """
        Вводит текст в поле 'Кому'
        :param whoam: Вводимый текст
        """
        if self.editable(selector=self._whoam_field):
            self.typing(selector=self._whoam_field, text=whoam)

    @allure.step("Ввести тему в поле 'Тема'")
    def typing_topic(self, topic: str) -> None:
        """
        Вводит текст в поле 'Тема'
        :param topic: Вводимый текст
        """
        self.click(selector=self._topic_field)
        if self.editable(selector=self._whoam_field):
            self.typing(selector=self._topic_field, text=topic)

    @allure.step("Ввести текст письма")
    def typing_message(self, text: str) -> None:
        """
        Вводит текст письма
        :param text: Вводимый текст
        """
        self.click(selector=self._message_field)
        if self.editable(selector=self._whoam_field):
            self.typing(selector=self._message_field, text=text)

    @allure.step("Нажать на кнопку 'Отправить'")
    def send_message(self) -> None:
        """
        Нажимает на кнопу 'Отправить'
        :return:
        """
        if self.clickable(selector=self._send_message_button):
            self.click(selector=self._send_message_button)

    def get_text_in_topic(self) -> str:
        """
        Получает текст темы письма
        :return:
        """
        return self.get_element(selector=self._topic_field).input_value()

    def get_text_in_whoam(self) -> str :
        """
        Получает текст из поля 'Кому'
        :return:
        """
        return self.get_element(selector=self._whoam_field).input_value()

    def get_text_in_message(self) -> str:
        """
        Получает текст из письма
        :return:
        """
        return self.get_element(selector=self._message_field).input_value()

    def get_text_in_label(self, text) -> str:
        """
        Получает текст уведомлений при отправке
        :param text: Текст уведомления
        :return:
        """
        return self.get_element(selector=self._label(text)).inner_text()
