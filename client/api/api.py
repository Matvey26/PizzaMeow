"""Класс текущей сессии, который предоставляет возможность общения """

import config
import requests

class Session:
    succefuly_authorization = False
    def __init__(self):
        if config.user_pass != None and config.user_login != None and config.user_id != None:
            params = {'user_id' : config.user_id,
                      'user_pass' : config.user_pass,
                      'user_login' : config.user_login,
                      'user_email' : config.user_email}
            try:
                response = requests.get("our server adress", params=params)
            except requests.ConnectionError:
                print("Подключение не установлено")
                return 
            if response == 200:
                print("Авторизация прошла успешно! Щас вас трахнут")
                # получаем контент хз что
                return 
        print("Автоматическая авторизация прошла не успешна")
        answer = None
        while (answer != "Авторизоваться" or answer != "Выйти" or answer != "Зарегистрироваться"):
            answer = str(input("Если у вас есть аккаунт - введите: Авторизоваться, иначе - Зарегистрироваться"))
            if (answer == "Авторизоваться"):
                email = str(input("Введите почту"))
                login = str(input("Введите логин"))
                password = str(input("Введите пароль"))
                try:
                    sign_in(email, login, password, user_id)
                except requests.ConnectionError:
                    print("Интернет проблема, напишите - Выйти или придется повторить подклчение")
                    answer = None
            elif (answer == "Зарегистрироваться"):
                email = str(input("Введите почту"))
                login = str(input("Придумайте логин"))
                password = str(input("Придумайте пароль"))  
                try:      
                    sign_up(email, login, password, user_id)
                except requests.ConnectionError:
                    print("Интернет проблема, напишите - Выйти или придется повторить подклчение")
                    answer = None
            else:
                print("Хватит ставить клоуна, введите корректно, иначе напишите - Выйти")

    def sign_up(self, email: str, login: str, password: str, id=None):
        

        """Регистрирует нового пользователя"""

    def sign_in(self, email, login, password, id=None):
        p
        """Авторизоваться на сервере, то есть получить access token и сохранить его в приложении"""
