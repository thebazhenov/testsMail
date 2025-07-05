import allure
import pytest

from conftest import USER_LOGIN, login_in_system


@pytest.fixture(scope="function")
def open_send_letter_page(base_test, login_in_system):
    base_test.main_page.open_window_letter()
    return login_in_system


@pytest.fixture(scope="function", autouse=False)
def send_letter(base_test, open_send_letter_page, request):
    params = request.param if hasattr(request, 'param') and isinstance(request.param, dict) else {}
    whoam = params.get("whoam", USER_LOGIN)
    topic = params.get("topic", "test topic")
    message = params.get("message", "test message")
    base_test.write_letter_page.typing_whoam(whoam=whoam)
    base_test.write_letter_page.typing_topic(topic=topic)
    base_test.write_letter_page.typing_message(text=message)
    base_test.write_letter_page.send_message()
    return params if hasattr(request, "param") else {"whoam": USER_LOGIN, "topic": topic, "message": message}

@pytest.mark.ui
@pytest.mark.full_regression
@allure.epic("WriteLetterPageUI")
class TestWriteLetter:

    @pytest.mark.parametrize(
        "allure_title, whoam",
        [
            pytest.param("Заполнение поля 'Кому'", USER_LOGIN,marks=pytest.mark.critical),
            ("Test", "testuser@gmail.com")
        ]
    )
    def test_typing_whoam(self, base_test, open_send_letter_page, allure_title, whoam: str):
        base_test.write_letter_page.typing_whoam(whoam=whoam)
        assert base_test.write_letter_page.get_text_in_whoam() == whoam

    @pytest.mark.parametrize(
        "allure_title, topic",
        [
            pytest.param("Заполнение поля 'Тема'", "Test topic")
        ]
    )
    def test_typing_topic(self, base_test, open_send_letter_page, allure_title, topic: str):
        base_test.write_letter_page.typing_topic(topic=topic)
        assert base_test.write_letter_page.get_text_in_topic() == topic

    @pytest.mark.parametrize(
        "allure_title, message",
        [
            pytest.param("Заполнение текста письма", "test message")
        ]
    )
    def test_typing_message(self, base_test, open_send_letter_page, allure_title, message: str):
        base_test.write_letter_page.typing_message(text=message)
        assert base_test.write_letter_page.get_text_in_message() == message

    @pytest.mark.parametrize(
        "allure_title, send_letter",
        [
            ("Отправка письмама", {"login": USER_LOGIN, "topic": "topic", "message": "message"})
        ],
        indirect=["send_letter"]
    )
    def test_send_message(self, base_test, open_send_letter_page, delete_all_message, allure_title: str,
                          send_letter):
        allure.dynamic.title(allure_title)
        with allure.step("Отправить письмо, заполнив все данные"):
            assert base_test.write_letter_page.get_text_in_label(text="Отправка сообщения...") == "Отправка сообщения..."
            assert base_test.write_letter_page.get_text_in_label(text="Сообщение отправлено") == "Сообщение отправлено."
