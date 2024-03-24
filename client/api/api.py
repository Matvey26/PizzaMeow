"""Класс текущей сессии, который предоставляет возможность общения """

import requests
import os
url = 'http://127.0.0.1:8000/api/'

class Session:
    def __init__(self):
        pass
    # Вова передает мне аргументы формата пароль почту из его кэша
    def sign_in(self, email : str, password : str):
        params = {'email' : email, 'password' : password}
        try:
            response = requests.get(url + 'auth', params=params)
            if response.status_code == 200:
                self.password = password
                self.email = email
                self.token = response.text
                return response.text
            return response.status_code
            # если данные не верны вова должен заставить человека авторизоваться вручную
        except requests.ConnectionError:
            return -1 # означает что проблема с интернетом у пользователя

    def sign_up(self, email: str, password : str):
        params = {'email' : email, 'password' : password}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url + 'register', json=params, headers=headers)
            if response.status_code == 200:
                self.password = password
                self.email = email
                self.token = response
                return response.text
            return response.status_code
        except requests.ConnectionError:
            return -1 # подключение прошло не успешно
    def get_pizzas(self, limit : int, offset : int):
        params = {'limit' : limit, 'offset' : offset}
        try:
            response.get(url + 'pizzas', params=params)
            if response.status_code == 400:
                return response.json()
            return response.status_code
        except requests.ConnectionError:
            return -1
    def whoami(self):
        
    # пользователь про себя данные вносит
    def user_defenition(self, name : str, surname : str, adress : str, card : str):
        params = {'status' : 'defenition',
                  'user_id' : self.user_id,
                  'user_name' : name,
                  'user_surname' : surname,
                  'user_adress' : adress,
                  'user_card' : card}
        try:
            response = requests.patch("matvey_server.com", params=params) # в случае удачи вернут True иначе False
            return response
        except requests.ConnectionError:
            return -1
    
    def get_history(self):
        params = {'status' : 'history', 'user_id' : self.user_id}
        try:
            response = requests.get("matvey_server.com", params=params)
            return response # хочу чтоб вернуло словарик из cловарика(aйди - результирующая цена, ингридиент - цена....) - дата
        except requests.ConnectionError:
            return -1 # интернет
    
    def change(self, email, login, password, newdata): # newdata = ['одна из возможных  параметров пользователя в точности как в запросах предыдущих'б новое значение] вова должен мне сказать что хочется поменять кроме id
        status = sign_in(email, login, password)
        if status == -1:
            return -1
        elif status == 0:
            return 0 # чел ввел не те данные
        else:
            param = {'status' : 'changepassword', newdata[0] : newdata[1]}
            try:
                response = requests.patch("matvey_server.com", params=params)
                return response # 1 если успешно 0 неудача
            except requests.ConnectionError:
                return -1
    
    def check_active_orders(self):
        params = {'status' : 'get_active_orders', 'user_id' : self.user_id}
        try:
            response = requests.get("matvey_server.com", params=params)
            return response # 0  в случае если нет заказов активных иначе просто срез из user_history где дата сравнивается
        except requests.ConnectionError:
            return -1 # интернет

    def delete_order(self, id):
        params = {'status' : 'delete_order', 'user_id' : self.user_id, 'id_order' : id }
        try: 
            response = requests.patch("matvey_server.com", params=params)
            return response # 1 если успешно 0 неудача
        except requests.ConnectionError:
            return -1
    
    def make_order(self, order): # order состоит из ингридиентов цены и даты заказа \
        params = {'status' : 'make_order', 'user_id' : self.id, 'order' : order}
        try: 
            response = requests.patch("matvey_server.com", params=params)
            return response # id заказа если успешно 0 неудача
        except requests.ConnectionError:
            return -1


ses = Session()