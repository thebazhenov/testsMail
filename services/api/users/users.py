import smtplib
from email.mime.text import MIMEText
from os import login_tty

import allure

from requests import Response
from services import BaseApiClient


class Users(BaseApiClient):

    def create_new_user(self, **kwargs) -> Response:
        """
        Метод создания пользователя
        :param data: json in body
        :return: Response
        """
        response = self._request(method="POST", endpoint="/api/user", **kwargs)
        return response

    def gets_current_greenmail_users(self) -> Response:
        """
        Метод получения списка пользователей
        :return: Response
        """
        response = self._request(method="GET", endpoint="/api/user")
        return response

    def delete_given_user(self, user_email: str) -> Response:
        """
        Метод удаления пользователя
        :param user_email: email пользователя
        :return: Response
        """
        response = self._request(method="DELETE", endpoint=f"/api/user/{user_email}")
        return response

    def gets_the_message_for_given_user_and_folder(self, user_email: str, name_folder: str = None) -> Response:
        """
        Метод получения сообщений пользователя
        :param user_email:
        :param name_folder:
        :return:
        """
        response = self._request(method="GET", endpoint=f"/api/user/{user_email}/messages/{name_folder}")
        return response

    @staticmethod
    def check_user(users, current_login, current_email) -> dict | bool:
        for user in users:
            user_login = user.get("login")
            user_email = user.get("email")
            if user_login == current_login and current_email == user_email:
                return user
        return False

    @staticmethod
    def form_letter(email_from: str, email_to: str,
                   subject: str, text: str):
        msg = MIMEText(text)
        msg["Subject"] = subject
        msg["From"] = email_from
        msg["To"] = email_to

        return msg

    def send_email(self, login: str, email_to: str, password: str):
        smtp_host = "localhost"
        smtp_port = 3025
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.login(login, password)
            msg = self.form_letter(email_from=login,
                                   email_to=email_to,
                                   subject="Test",
                                   text="Test letter")
            server.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg.as_string())
            print("letter sending")

