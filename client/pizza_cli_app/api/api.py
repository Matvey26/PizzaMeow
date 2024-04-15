"""Класс текущей сессии, предоставляющий удобный интерфейс взаимодействия клиента с сервером."""

import requests
import os
import pathlib
import json
url = 'http://127.0.0.1:8000/api/'


def connection_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError:
            return (-1, 'Ошибка соединения')
        
    return wrapper


class Session:
    def __init__(self):
        save_dir = pathlib.Path(__file__).parent.parent  # Папка pizza_cli_app
        save_path = save_dir / '.saved_token.json'
        save_path.touch()
        if save_path.stat().st_size == 0:
            with save_path.open('w') as file:
                json.dump({'token': ''}, file)
        with save_path.open('r') as file:
            self.__token = json.load(file).get('token', '')

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value
        save_dir = pathlib.Path(__file__).parent.parent  # Папка pizza_cli_app
        save_path = save_dir / '.saved_token.json'
        save_path.touch()
        if save_path.stat().st_size == 0:
            with save_path.open('w') as file:
                json.dump({'token': ''}, file)
        with save_path.open('w') as file:
            json.dump({'token': self.token}, file)

    @connection_error_handler
    def sign_in(self, email: str, password: str):
        """По данным регистрационным данным запрашивает у сервера токен доступа.
        
        Параметры
        ---------
        email: str
            Почта, привязанная к аккаунту
        password: str
            Пароль от аккаунта

        Возвращает
        ----------
        error_message: tuple
            Кортеж из кода состояния ответа и сообщение об ошибке
        ничего
            Если запрос был обработан успешно, функция ничего не возвращает
        """

        params = {'email' : email, 'password' : password}
        response = requests.get(url + 'users/signin', params=params)
        if response.status_code == 200:
            self.password = password
            self.email = email
            self.token = response.text
            return
        data = json.loads(response.text)
        return (response.status_code, data['detail'])

    @connection_error_handler
    def sign_up(self, email: str, password : str):
        """Регистрирует новый аккаунт.
        
        Параметры
        ---------
        email: str
            Почта, которая будет привязана к аккаунту (которая будет использоваться при входе)
        password: str
            Пароль от аккаунта

        Возвращает
        ----------
        error_message: tuple
            Кортеж из кода состояния ответа и сообщение об ошибке
        ничего
            Если запрос был обработан успешно, функция ничего не возвращает
        """
        params = {'email' : email, 'password' : password}
        response = requests.post(url + 'users/signup', json=params)
        if response.status_code == 200:
            self.password = password
            self.email = email
            self.token = response.text
            return
        data = json.loads(response.text)
        return (response.status_code, data['detail'])

    def logout(self):
        self.token = ''

    @connection_error_handler
    def config(self, data: dict):
        """Принимает словарь с данными, которые нужно обновить."""
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = requests.patch(url + 'users/config/update', json=data, headers=headers)
        if response.status_code != 204:
            data = json.loads(response.text)
            return (response.status_code, data['detail'])

    @connection_error_handler
    def add_card(self, data):  # под датой словарь  
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = response.post(url + 'users/config/addcard', json=data, headers=headers)
        return response.status_code

    @connection_error_handler
    def add_pizza(self, data): # под датой словарь
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = response.post(url + '/carts', json=data, headers=headers)
        return response.status_code

    @connection_error_handler
    def create_order(self, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = response.post(url + '/orders', json=data, headers=headers)
        if response.status_code == 200:
            return response.text # ссылка на оплату
        return response.status_code

    @connection_error_handler
    def get_pizzas(self, limit : int, offset : int):
        params = {'limit' : limit, 'offset' : offset}
        response = response.get(url + 'pizzas', params=params)
        if response.status_code == 200:
            return response.json()
        return response.status_code

    @connection_error_handler
    def id_pizza(self, id : int):
        response = response.get(url + f'pizzas/{id}')
        if response.status_code == 200:
            return response.json()
        return response.status_code

    @connection_error_handler
    def get_orders(self, limit : int, offset : int):
        params = {'limit' : limit, 'offset' : offset}
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = response.get(url + 'orders', headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return response.status_code

    @connection_error_handler
    def id_order(self, id : int):
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = response.get(url + f'orders/{id}', headers=headers)
        if response.status_code == 200:
            return response.json()
        return response.status_code
    
    @connection_error_handler
    def get_cart(self):
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = response.get(url + 'carts', headers=headers)
        if response.status_code == 200:
            return response.json()
        return response.status_code

    @connection_error_handler
    def get_time(self, address : str):
        params = {'address' : address}
        response = response.get(url + 'delivery/time', params=params)
        if response.status_code == 200:
            return response.text
        return response.status_code

    @connection_error_handler
    def new_item(self, id : int, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = response.patch(url + f'carts/{id}',  json=data, headers=headers)
        return response.status_code
    
    @connection_error_handler
    def change_password(self, params : str):
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = response.put(url + 'users/change_password', headers=headers, params=params)
        return response.status_code

    @connection_error_handler
    def reset_password(self, params : str):
        response = response.put(url + 'users/reset_password', params=params)
        return response.status_code

    @connection_error_handler
    def change_email(self, params : str):
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = response.put(url + 'users/change_email', headers=headers, params=params)
        return response.status_code

    @connection_error_handler
    def change_item(self, id : int, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = response.put(url + f'carts/{id}', json=data, headers=headers)
        return response.status_code
    
    @connection_error_handler
    def delete_item(self, id : int):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = response.delete(url + f'carts/{id}', headers=headers)
        return response.status_code