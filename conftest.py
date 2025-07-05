import os
import pytest
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright
from datetime import datetime

from config.base_test import BaseTest
from services import MAIL_URL

load_dotenv()

USER_LOGIN = os.getenv("USER_LOGIN")
USER_PASSWORD = os.getenv("USER_PASSWORD")

# Папка для скриншотов
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")


def pytest_addoption(parser):
    """
    Добавление опции --browser / -B
    """
    parser.addoption(
        "--browser", "-B",
        action="append",
        help="Browser(s) to run tests against. Use 'all' or repeat: -B chromium -B firefox"
    )


def pytest_generate_tests(metafunc):
    """
    Генерация parametrize для фикстуры browser_name
    """
    if "browser_name" in metafunc.fixturenames:
        browsers = metafunc.config.getoption("browser")

        if not browsers or "all" in browsers:
            browsers = ["chromium", "firefox", "webkit"]

        metafunc.parametrize("browser_name", browsers, scope="session")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    По окончании каждого этапа теста (setup/call/teardown) проверяем,
    упал ли основной вызов (when == "call"). Если упал — сохраняем скриншот.
    """
    outcome = yield
    rep = outcome.get_result()

    # интересует именно основной вызов теста
    if rep.when == "call" and rep.failed:
        # пытаемся достать fixture "page"
        page = item.funcargs.get("page", None)
        if page:
            # убедимся, что папка есть
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            # имя файла: <testname>-<timestamp>.png
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"{item.name[:20]}-{timestamp}.png"
            path = os.path.join(SCREENSHOT_DIR, filename)

            # снимаем скриншот всего экрана
            page.screenshot(path=path, full_page=True)
            # логируем, чтобы было видно в выводе pytest
            print(f"\n[Screenshot saved] {path}")

            # Прикрепление в отчет скриншота
            try:
                import allure
                allure.attach.file(
                    path,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except ImportError:
                pass


@pytest.fixture(scope="session")
def browser(browser_name):
    with sync_playwright() as playwright:
        browser = getattr(playwright, browser_name).launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        locale="ru-RU"
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def base_test(page) -> BaseTest:
    """
    Создает объект класса для использования в тестах
    :param page: Фикстура
    :return: Объект класса BaseTest
    """
    return BaseTest(page)

@pytest.fixture(scope="function")
def delete_all_message(base_test):
    """
    Удаляет все письма
    :param base_test: Фикстура
    :return:
    """
    response = base_test.system.purges_all_mails()
    assert response.status_code == 200

@pytest.fixture(scope="function")
def login_in_system(request, base_test, delete_all_message):
    """
    Авторизуется на сайте
    :param request: Возможность параметризовать
    :param base_test: Фикстура
    :param delete_all_message: Очищает данные перед выполнением авторизации
    :return:
    """
    params = request.param if hasattr(request, 'param') and isinstance(request.param, dict) else {}
    user_login = params.get("login", USER_LOGIN)
    user_password = params.get("password", USER_PASSWORD)
    base_test.login_page.open(url=MAIL_URL)
    base_test.login_page.login(email=user_login, password=user_password)

    return params if hasattr(request, "param") else {"login": USER_LOGIN, "password": USER_PASSWORD}
