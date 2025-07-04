from services import System, API_URL
from services.ui import *

class BaseTest:

    def __init__(self, page):
        self.page = page

    def _get_lazy_instance(self, attr_name: str, cls, use_page: bool = True):
        if not hasattr(self, attr_name):
            if use_page:
                setattr(self, attr_name, cls(page=self.page))
            else:
                setattr(self, attr_name, cls(base_url=API_URL))  # Создаем экземпляр без page
        return getattr(self, attr_name)

    @property
    def login_page(self) -> LoginPage:
        return self._get_lazy_instance("_login_page", LoginPage)

    @property
    def main_page(self) -> MainPage:
        return self._get_lazy_instance("_main_page", MainPage)

    @property
    def write_letter_page(self) -> WriteLetterPage:
        return self._get_lazy_instance("_write_letter_page", WriteLetterPage)

    @property
    def base_page(self) -> BasePage:
        return self._get_lazy_instance("_base_page", BasePage)

    @property
    def system(self) -> System:
        return self._get_lazy_instance("_system", System, use_page=False)
