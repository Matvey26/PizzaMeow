"""Класс текущей сессии, который предоставляет возможность общения """

import config
import requests

class Session:
    def __init__(self):
        if config.user_pass != None and config.user_login != None and config.user_id != None:
            params = {'user_id' : config.user_id,
                      'user_pass' : config.user_pass,
                      'user_login' : config.user_login}
            response = requests.get("our server adress", params=params)
            if response == 200:
                response.content


    def sign_up(self, login: str, password: str):
        """Регистрирует нового пользователя"""

    def sign_in(self, login, password):
        """Авторизоваться на сервере, то есть получить access token и сохранить его в приложении"""
