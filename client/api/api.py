"""Класс текущей сессии, который предоставляет возможность общения """

import config
import requests
import os

class Session:
    def __init__(self):
        hostname = "matvey_server.com"
        response = os.system("ping -c 1 " + hostname)
        if (response == 0):
            pass
        else:
            raise requests.ConnectionError("Connection Error") # сессия не создастся
    # Вова передает мне аргументы формата логин пароль id пользователя из его кэша
    def authothication(self, email, login, password, id):
        params = {'status' : 'authorization',
                  'user_id' : id,
                  'user_pass' : password,
                  'user_login' : login,
                  'user_email' : email}
        try:
            response = requests.get("matvey_server.com", params=params) # здесь я считаю, что будет или 0 - то есть подключение успешно установлено, или 2 то есть неправильные данные человека
            if response == 0:
                self.user_id = id
                self.user_password = password
                self.user_email = email
                self.user_login = login
                return 0
            return 2
            # если данные не верны вова должен заставить человека авторизоваться вручную
        except requests.ConnectionError:
                return -1 # означает что проблема с интернетом у пользователя
    def sign_up(self, email, login, password):
        params = {'status' : 'regestration',
                  'user_id' : None, # здесь он None я хочу чтобы мне вернули его id(я запишу его себе и вове отдам) в случае не удачи верну 0(то есть id человек начнется с 1)
                  'user_pass' : password,
                  'user_login' : login,
                  'user_email' : email}
        try:
            response = requests.get("matvey_server.com", params=params)
            if response != 0:
                self.user_id = id
                self.user_password = password
                self.user_email = email
                self.user_login = login
                self.id = response
            # неудача - если email уже например уже есть 
                return response
        except requests.ConnectionError:
            return -1 # например означает что интернет того 

    def sign_in(self, email, login, password):
        params = {'status' : 'sign_in',
                  'user_id' : None, # хочу получить айди человека в случае неудачи - 0  у человека не может быть адишника в кэше но может быть знание ост данных(допустим как в игру зашел с другого пк)
                  'user_pass' : password,
                  'user_login' : login,
                  'user_email' : email}
        try:
            response = requests.get("matvey_server.com", params=params)
            if response != 0:
                self.user_id = response
                self.user_password = password
                self.user_email = email
                self.user_login = login
                self.id = response
            return response
        except requests.ConnectionError:
            return -1 # аналогично
    # пользователь про себя данные вносит
    def user_defenition(self, name, surname, adress, card):
        params = {'status' : 'defenition',
                  'user_id' : self.user_id,
                  'user_name' : name,
                  'user_surname' : surname,
                  'user_adress' : adress,
                  'user_card' : card}
        try:
            response = requests.get("matvey_server.com", params=params) # в случае удачи вернут True иначе False
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
                response = requests.get("matvey_server.com", params=params)
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
            response = requests.get("matvey_server.com", params=params)
            return response # 1 если успешно 0 неудача
        except requests.ConnectionError:
            return -1




