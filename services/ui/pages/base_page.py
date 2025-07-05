from playwright.sync_api import Page, ElementHandle, Locator
from playwright.sync_api import Error


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def open(self, url) -> None:
        """
        Открывает указанный url
        :param url: Адрес, который необходимо открыть
        """
        self.page.goto(url)

    def clickable(self, selector: str, timeout: int = 30000) -> bool:
        """
        Проверяет, что элемент отображается и является кликабельным
        :param selector: Локатор
        :param timeout: Время ожидания локатора
        :return: В случае, если условие выполняется True, иначе None
        """
        try:
            if self.page.is_visible(selector, timeout=timeout) and self.page.is_enabled(selector, timeout=timeout):
                return True
        except Exception:
            raise ValueError("Локатор не найден или не кликабелен")


    def check_element_on_website(self, selector: str, timeout: int = 30000) -> ElementHandle:
        """
        Проверяет наличие элемента на странице
        :param selector: Локатор
        :param timeout: Время ожидания появления локатора
        :return: Объект класса ElementHandle
        """
        try:
            return self.page.wait_for_selector(selector, timeout=timeout)
        except Exception:
            raise ValueError("Локатор не найден")

    def typing(self, selector: str, text: str) -> None:
        """
        Ввод текста
        :param selector: Локатор
        :param text: Вводимый текст
        """
        if self.editable(selector=selector):
            self.page.type(selector=selector, text=text)

    def click(self, selector: str) -> None:
        """
        Клик по элементу
        :param selector: Локатор
        """
        self.check_element_on_website(selector=selector)
        if self.clickable(selector):
            self.page.click(selector)
        else:
            raise ValueError("Локатор не найден или не кликабелен")

    def get_element(self, selector: str, **kwargs) -> bool | Locator:
        """
        Получить элемент по локатору
        :param selector: Локатор
        :param kwargs:
        :return: Объект класса Locator | False, если элемент не найден
        """
        if not self.check_element_on_website(selector):
            return False
        return self.page.locator(selector, **kwargs)

    def editable(self, selector) -> bool:
        """
        Проверка на то, что элемент редактируемый
        :param selector:
        :return:
        """
        return self.get_element(selector=selector).is_editable()

    def attached(self, selector):
        return self.get_element(selector=selector).wait_for(state="attached")

    def wait_page(self, url_pattern: str):
        """
        Ожидание появление url
        :param url_pattern:
        """
        return self.page.wait_for_url(url=f"{url_pattern}")

    @staticmethod
    def get_attribute(element: Locator, name: str) -> str | None:
        """
        Возвращает значение указанного атрибута элемента
        :param element: Объект класса локатор
        :param name: Название атрибута
        """
        return element.get_attribute(name)

    @property
    def get_current_url(self) -> str:
        """
        Получение текущего url
        :return: url
        """
        return self.page.url
