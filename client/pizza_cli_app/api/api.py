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
            response = requests.get(url + 'users/signin', params=params)
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
        try:
            response = requests.post(url + 'users/signup', json=params)
            if response.status_code == 200:
                self.password = password
                self.email = email
                self.token = response
                return response.text
            return ('Неверный пароль', response.status_code)
        except requests.ConnectionError:
            return -1 # подключение прошло не успешно

    def add_card(self, data):  # под датой словарь  
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        try:
            response = response.post(url + 'users/config/addcart', json=data, headers=headers)
            return response.status_code
        except requests.ConnectionError:
            return -1

    def add_pizza(self, data): # под датой словарь
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        try:
            response = response.post(url + '/carts', json=data, headers=headers)
            return response.status_code
        except requests.ConnectionError:
            return -1

    def create_order(self, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        try:
            response = response.post(url + '/orders', json=data, headers=headers)
            if response.status_code == 200:
                return response.text # ссылка на оплату
            return response.status_code
        except requests.ConnectionError:
            return -1

    def get_pizzas(self, limit : int, offset : int):
        params = {'limit' : limit, 'offset' : offset}
        try:
            response = response.get(url + 'pizzas', params=params)
            if response.status_code == 200:
                return response.json()
            return response.status_code
        except requests.ConnectionError:
            return -1

    def id_pizza(self, id : int):
        try:
            response = response.get(url + f'pizzas/{id}')
            if response.status_code == 200:
                return response.json()
            return response.status_code
        except requests.ConnectionError:
            return -1

    def whoami(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = requests.get(url + 'whoami', headers=headers)
            if response.status_code == 200:
                return response.json()
            return response.status_code
        except requests.ConnectionError:
            return -1

    def get_orders(self, limit : int, offset : int):
        params = {'limit' : limit, 'offset' : offset}
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = response.get(url + 'orders', headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            return response.status_code
        except requests.ConnectionError:
            return -1

    def id_order(self, id : int):
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = response.get(url + f'orders/{id}', headers=headers)
            if response.status_code == 200:
                return response.json()
            return response.status_code
        except requests.ConnectionError:
            return -1
        
    def get_cart(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = response.get(url + 'carts', headers=headers)
            if response.status_code == 200:
                return response.json()
            return response.status_code
        except requests.ConnectionError:
            return -1

    def get_time(self, address : str):
        params = {'address' : address}
        try: 
            response = response.get(url + 'delivery/time', params=params)
            if response.status_code == 200:
                return response.text
            return response.status_code
        except requests.ConnectionError:
            return -1
    
    def update(self, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        try:
            response = response.patch(url + 'users/config/update', json=data, headers=headers)
            return response.status_code
        except requests.ConnectionError:
            return -1

    def new_item(self, id : int, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        try:
            response = response.patch(url + f'carts/{id}',  json=data, headers=headers)
            return response.status_code
        except requests.ConnectionError:
            return -1
        
    def change_password(self, params : str):
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = response.put(url + 'users/change_password', headers=headers, params=params)
            return response.status_code
        except requests.ConnectionError:
            return -1

    def reset_password(self, params : str):
        try:
            response = response.put(url + 'users/reset_password', params=params)
            return response.status_code
        except requests.ConnectionError:
            return -1

    def change_email(self, params : str):
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = response.put(url + 'users/change_email', headers=headers, params=params)
            return response.status_code
        except requests.ConnectionError:
            return -1

    def change_item(self, id : int, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        try:
            response = response.put(url + f'carts/{id}', json=data, headers=headers)
            return response.status_code
        except requests.ConnectionError:
            return -1
    def delete_item(self, id : int):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        try:
            response = response.delete(url + f'carts/{id}', headers=headers)
            return response.status_code
        except requests.ConnectionError:
            return -1


ses = Session()