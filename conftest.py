import os
import pytest
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright

from config.base_test import BaseTest
from services import Users, API_URL, MAIL_URL
from services.api.system.models import Message

load_dotenv()

USER_LOGIN = os.getenv("USER_LOGIN")
USER_PASSWORD = os.getenv("USER_PASSWORD")


@pytest.fixture(params=["chromium", "firefox", "webkit"], scope="session")
def browser(request):
    browser_name = request.param
    with sync_playwright() as playwright:
        browser = getattr(playwright, browser_name).launch(headless=False, )
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
        is_mobile=False,
        locale="ru-RU"
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session")
def user_api():
    """Объект API"""
    return Users(base_url=API_URL)


@pytest.fixture(scope="function", autouse=False)
def search_user(user_api, request):
    """Поиск пользователя"""
    params = request.param if hasattr(request, "param") else {}
    login = params.get("login", USER_LOGIN)
    email = params.get("email", USER_LOGIN)

    response = user_api.gets_current_greenmail_users()
    assert response.status_code == 200

    user = user_api.check_user(users=response.json(), current_login=login, current_email=email)
    return {"user": user, "response": response.json()} or False


@pytest.fixture(scope="function", autouse=False)
def delete_user(user_api, request):
    """
    Параметризуемое удаление пользователя после теста.
    Используется через indirect параметризацию.
    """
    params = request.param if isinstance(request.param, dict) else {}
    email = params.get("email", USER_LOGIN)

    yield  # тест выполняется до этой точки

    if email:
        response = user_api.delete_given_user(user_email=email)
        assert response.status_code == 200, response.json()
        assert Message(**response.json())


@pytest.fixture(scope="function", autouse=False)
def create_user(user_api, request):
    """Создание пользователя"""
    params = request.param if isinstance(request.param, dict) else {}
    login = params.get("login", USER_LOGIN)
    email = params.get("email", USER_LOGIN)
    password = params.get("password", USER_PASSWORD)

    payload = {
        "login": login,
        "email": email,
        "password": password
    }

    response = user_api.create_new_user(json=payload)
    assert response.status_code == 200, response.json()

    return {
        "response": response.json(),
        "login": login,
        "email": email,
        "password": password
    }


@pytest.fixture(scope="function")
def prepare_user(request, search_user, create_user):
    """
    Подготовка пользователя:
    если найден — удалить и создать заново
    """
    params = request.param if isinstance(request.param, dict) else {}
    email = params.get("email", USER_LOGIN)
    login = params.get("login", USER_LOGIN)

    if search_user:
        user_api = Users(base_url=API_URL)
        response = user_api.delete_given_user(user_email=email)
        assert response.status_code == 200
        assert Message(**response.json())

    return create_user

@pytest.fixture(scope="function")
def base_test(page) -> BaseTest:
    return BaseTest(page)

@pytest.fixture(scope="function")
def login_in_system(request, base_test):
    params = request.param if hasattr(request, 'param') and isinstance(request.param, dict) else {}
    user_login = params.get("login", USER_LOGIN)
    user_password = params.get("password", USER_PASSWORD)
    base_test.login_page.open(url=MAIL_URL)
    base_test.login_page.login(email=user_login, password=user_password)

    return params if hasattr(request, "param") else {"login": USER_LOGIN, "password": USER_PASSWORD}