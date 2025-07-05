from services.api import System, Users
from services.ui import *
from services import API_URL


class BaseTest:
    """
    Позволяет использовать все тестовые классы для работы
    """

    def __init__(self, page):
        self.page = page

    def _get_lazy_instance(self, attr_name: str, cls, use_page: bool = True):
        """
        Создает единожды объект класса
        :param attr_name: Имя под которым кэшируется объект,
        :param cls: Объект какого класса необходимо создать
        :param use_page: api | ui класс
        :return: Объект класса
        """
        private_name = f"_{attr_name}"
        if not hasattr(self, private_name):
            if use_page:
                setattr(self, private_name, cls(page=self.page))
            else:
                # Создаем экземпляр без page
                setattr(self, private_name, cls(base_url=API_URL))
        return getattr(self, private_name)

    @property
    def login_page(self) -> LoginPage:
        """
        Создает объект класса LoginPage,
        :return: LoginPage объект
        """
        return self._get_lazy_instance("login_page", LoginPage)

    @property
    def main_page(self) -> MainPage:
        return self._get_lazy_instance("main_page", MainPage)

    @property
    def write_letter_page(self) -> WriteLetterPage:
        return self._get_lazy_instance("write_letter_page", WriteLetterPage)

    @property
    def base_page(self) -> BasePage:
        return self._get_lazy_instance("base_page", BasePage)

    @property
    def system(self) -> System:
        return self._get_lazy_instance("system", System, use_page=False)

    @property
    def users(self) -> Users:
        return self._get_lazy_instance("users", Users, use_page=False)
