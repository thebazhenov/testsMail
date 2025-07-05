import pytest, allure

from conftest import USER_LOGIN, USER_PASSWORD
from services.api.system.models import Message
from services.api.users.models import UserModel


@pytest.fixture(scope="function", autouse=False)
def send_letter_smtp(request, base_test, delete_all_message):
    params = request.param if hasattr(request, 'param') and isinstance(request.param, dict) else {}
    base_test.users.send_email(
        email_from=params.get("email_from", USER_LOGIN),
        email_to=params.get("email_to", USER_LOGIN),
        password=params.get("password", USER_PASSWORD),
        topic=params.get("topic", "test"),
        text=params.get("text", "test")
    )


@pytest.fixture(scope="function", autouse=False)
def search_user(base_test, request):
    """Поиск пользователя"""
    params = request.param if hasattr(request, "param") else {}
    login = params.get("login", USER_LOGIN)
    email = params.get("email", USER_LOGIN)

    response = base_test.users.gets_current_greenmail_users()
    assert response.status_code == 200

    user = base_test.users.check_user(users=response.json(), target_login=login, target_email=email)
    return {"user": user, "response": response.json()} or False


@pytest.fixture(scope="function", autouse=False)
def delete_user(base_test, request):
    """
    Параметризуемое удаление пользователя после теста.
    Используется через indirect параметризацию.
    """
    params = request.param if isinstance(request.param, dict) else {}
    email = params.get("email", USER_LOGIN)

    yield  # тест выполняется до этой точки

    if email:
        response = base_test.users.delete_given_user(user_email=email)
        assert response.status_code == 200, response.json()
        assert Message(**response.json())


@pytest.fixture(scope="function", autouse=False)
def create_user(base_test, request):
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

    response = base_test.users.create_new_user(json=payload)
    assert response.status_code == 200, response.json()

    return {
        "response": response.json(),
        "login": login,
        "email": email,
        "password": password
    }

@pytest.mark.full_regression
@pytest.mark.api
@allure.epic("User")
class TestUsers:


    @pytest.mark.parametrize(
        "create_user, delete_user, allure_title",
        [
            pytest.param(
                {"login": "test_user", "email": "testing_user@localhost.com", "password": "test"},
                {"email": "testing_user@localhost.com"},
                "Создание пользователя с данными: login = test_user, email = testing_user@localhost.com, password = test",
                marks=pytest.mark.critical
            )
        ],
        indirect=["create_user", "delete_user"]
    )
    def test_create_user(self, create_user, delete_user, allure_title):
        with allure.step("Создание пользователя"):
            model = UserModel(**create_user.get("response"))
            assert model.login == create_user.get("login")
            assert model.email == create_user.get("email")

    @allure.title("Получение пользователей GET запросом")
    def test_gets_current_users(self, search_user):
        with allure.step("Получение пользователей"):
            response_json = search_user.get("response")
            for response in response_json:
                assert UserModel(**response), response_json

    @pytest.mark.parametrize(
        "create_user, allure_title",
        [
            ({"login": "test_user", "email": "testing_user@localhost.com", "password": "test"},
             "Удаление пользователей DELETE запросом")
        ],
        indirect=["create_user"]
    )
    def tests_delete_user(self, base_test, create_user, allure_title):
        allure.dynamic.title(allure_title)
        email = create_user.get("email")
        response = base_test.users.delete_given_user(user_email=email)
        assert response.status_code == 200, response.json()
        model = Message(**response.json())
        assert model.message == f"User '{email}' deleted"


