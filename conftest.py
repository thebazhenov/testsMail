import os
import pytest
from dotenv import load_dotenv

from services import Users, API_URL
from services.api.system.models import Message

load_dotenv()

USER_LOGIN = os.getenv("USER_LOGIN")
USER_PASSWORD = os.getenv("USER_PASSWORD")


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