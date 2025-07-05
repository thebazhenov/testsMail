import smtplib
import allure

from email.mime.text import MIMEText
from requests import Response
from services import BaseApiClient


class Users(BaseApiClient):

    @allure.step("Создать нового пользователя через POST запрос на endpoint /api/user")
    def create_new_user(self, **kwargs) -> Response:
        """
        Метод создания пользователя
        :param data: json in body
        :return: Response
        """
        response = self._request(method="POST", endpoint="/api/user", **kwargs)
        return response

    @allure.step("Получить список пользователей через GET запрос на endpoint /api/user")
    def gets_current_greenmail_users(self) -> Response:
        """
        Метод получения списка пользователей
        :return: Response
        """
        response = self._request(method="GET", endpoint="/api/user")
        return response

    @allure.step("Удалить пользователя через DELETE запрос на endpoint /api/user/{{user_email}}")
    def delete_given_user(self, user_email: str) -> Response:
        """
        Метод удаления пользователя
        :param user_email: email пользователя
        :return: Response
        """
        response = self._request(method="DELETE", endpoint=f"/api/user/{user_email}")
        return response

    @allure.step("""
    Получить сообщения пользователей через GET запрос на endpoint
    /api/user/{{user_email}}/messages/{{name_folder}}
    """)
    def gets_the_message_for_given_user_and_folder(self, user_email: str, name_folder: str = None) -> Response:
        """
        Метод получения сообщений пользователя
        :param user_email: email пользователя
        :param name_folder: название папки
        :return:
        """
        response = self._request(method="GET", endpoint=f"/api/user/{user_email}/messages/{name_folder}")
        return response

    @staticmethod
    def check_user(users, target_login, target_email) -> dict | bool:
        """
        Ищет пользователя в списке пользователей
        :param users: Список пользователей
        :param target_login: Целевой логин пользователя
        :param target_email: Целевой email пользователя
        :return: Пользователь | False
        """
        for user in users:
            user_login = user.get("login")
            user_email = user.get("email")
            if user_login == target_login and target_email == user_email:
                return user
        return False

    @staticmethod
    def form_letter(email_from: str, email_to: str,
                   subject: str, text: str):
        """
        Формирование письма
        :param email_from: От кого
        :param email_to: Кому
        :param subject: Тема
        :param text: Текст письма
        """
        msg = MIMEText(text)
        msg["Subject"] = subject
        msg["From"] = email_from
        msg["To"] = email_to

        return msg

    @allure.step("Отправка письма через библиотеку smtplib")
    def send_email(self, email_from: str, email_to: str, password: str, topic: str = "test", text: str = "test"):
        """
        Отправка письма
        :param email_from: От кого
        :param email_to: Кому
        :param password: Пароль от пользователя
        :param topic: Тема
        :param text: Текст письма
        :return:
        """
        smtp_host = "localhost"
        smtp_port = 3025
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.login(email_from, password)
            msg = self.form_letter(email_from=email_from,
                                   email_to=email_to,
                                   subject=topic,
                                   text=text)
            server.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
