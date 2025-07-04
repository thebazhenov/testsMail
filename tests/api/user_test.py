import pytest, allure
from conftest import create_user, delete_user, search_user, USER_LOGIN
from services import Users, API_URL
from services.api.system.models import Message
from services.api.users.models import UserModel


@pytest.mark.api
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

    def test_gets_current_users(self, search_user):
        with allure.step("Получение пользователей"):
            response_json = search_user.get("response")
            for response in response_json:
                assert UserModel(**response), response_json

    @pytest.mark.parametrize(
        "create_user",
        [
            {"login": "test_user", "email": "testing_user@localhost.com", "password": "test"}
        ],
        indirect=["create_user"]
    )
    def tests_delete_user(self, user_api, create_user):
        email = create_user.get("email")
        response = user_api.delete_given_user(user_email=email)
        assert response.status_code == 200, response.json()
        model = Message(**response.json())
        assert model.message == f"User '{email}' deleted"


