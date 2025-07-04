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
        # "//i[@class='icon']]//span"
    def typing_whoam(self, whoam: str):
        if self.editable(selector=self._whoam_field):
            self.typing(selector=self._whoam_field, text=whoam)

    def typing_topic(self, topic: str):
        self.click(selector=self._topic_field)
        if self.editable(selector=self._whoam_field):
            self.typing(selector=self._topic_field, text=topic)

    def typing_message(self, text: str):
        self.click(selector=self._message_field)
        if self.editable(selector=self._whoam_field):
            self.typing(selector=self._message_field, text=text)

    def send_message(self) -> None:
        if self.clickable(selector=self._send_message_button):
            self.click(selector=self._send_message_button)

    def get_text_in_topic(self):
        return self.get_element(selector=self._topic_field).input_value()

    def get_text_in_whoam(self):
        return self.get_element(selector=self._whoam_field).input_value()

    def get_text_in_message(self):
        return self.get_element(selector=self._message_field).input_value()

    def get_text_in_label(self, text):
        return self.get_element(selector=self._label(text)).inner_text()
