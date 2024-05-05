"""Класс текущей сессии, предоставляющий удобный интерфейс взаимодействия клиента с сервером."""

import requests
import os
import pathlib
import json
url = 'http://127.0.0.1:8000/api/'

pizzas = [
    {"id": 1, "name": "Margherita", "description": "Tomato, mozzarella, and basil.", "price": 8.0},
    {"id": 2, "name": "Pepperoni", "description": "Tomato, mozzarella, and pepperoni.", "price": 10.0},
    {"id": 3, "name": "BBQ Chicken", "description": "BBQ sauce, chicken, red onions, and cilantro.", "price": 12.0},
    {"id": 4, "name": "Veggie", "price": 11.0},
    {"id": 5, "name": "Hawaiian", "description": "Tomato, mozzarella, ham, and pineapple.", "price": 10.5},
    {"id": 6, "name": "Meat Lovers", "description": "Tomato, mozzarella, pepperoni, sausage, ham, and bacon.", "price": 13.0},
    {"id": 7, "name": "Margherita Deluxe", "description": "Tomato, mozzarella, cherry tomatoes, basil, and garlic.", "price": 9.0},
    {"id": 8, "name": "Buffalo Chicken", "description": "Buffalo sauce, chicken, ranch, and red onions.", "price": 12.5},
    {"id": 9, "name": "Cheese", "price": 7.0},
    {"id": 10, "name": "Supreme", "description": "Tomato, mozzarella, pepperoni, sausage, mushrooms, onions, and olives.", "price": 14.0},
    {"id": 11, "name": "Garden", "description": "Tomato, mozzarella, spinach, artichokes, and olives.", "price": 11.5},
    {"id": 12, "name": "Sausage", "description": "Tomato, mozzarella, and sausage.", "price": 10.5},
    {"id": 13, "name": "Bacon", "description": "Tomato, mozzarella, and bacon.", "price": 11.0},
    {"id": 14, "name": "Mushroom", "description": "Tomato, mozzarella, and mushrooms.", "price": 10.0},
    {"id": 15, "name": "Onion", "description": "Tomato, mozzarella, and onions.", "price": 9.5},
    {"id": 16, "name": "Black Olive", "description": "Tomato, mozzarella, and black olives.", "price": 9.5},
    {"id": 17, "name": "White", "description": "Garlic, mozzarella, and ricotta.", "price": 10.0},
    {"id": 18, "name": "Spinach", "description": "Garlic, mozzarella, spinach, and artichokes.", "price": 11.5},
    {"id": 19, "name": "Chicken Alfredo", "description": "Alfredo sauce, chicken, and mozzarella.", "price": 12.0},
    {"id": 20, "name": "Pesto", "description": "Pesto sauce, mozzarella, and cherry tomatoes.", "price": 11.0},
    {"id": 21, "name": "Taco", "description": "Taco sauce, ground beef, lettuce, and tomatoes.", "price": 11.5},
    {"id": 22, "name": "Seafood", "description": "Tomato, mozzarella, shrimp, calamari, and clams.", "price": 14.0},
    {"id": 23, "name": "Caprese", "description": "Tomato, mozzarella, basil, and balsamic glaze.", "price": 11.0},
    {"id": 24, "name": "Greek", "description": "Tomato, mozzarella, feta, kalamata olives, and red onions.", "price": 12.0},
    {"id": 25, "name": "Buffalo Cauliflower", "description": "Buffalo sauce, cauliflower, and ranch.", "price": 12.5}
]



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

    # ---------------- РАБОТА С УЧЁТНОЙ ЗАПИСЬЮ ПОЛЬЗОВАТЕЛЯ ---------------------

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
        return (response.status_code, response.json()['detail'])

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
        return (response.status_code, response.json()['detail'])

    def logout(self):
        self.token = ''

    @connection_error_handler
    def config(self, data: dict):
        """Принимает словарь с данными, которые нужно обновить."""
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        response = requests.patch(url + 'users/config', json=data, headers=headers)
        if response.status_code != 204:
            return (response.status_code, response.json()['detail'])
        
    @connection_error_handler
    def change_password(self, email: str, old_password: str, new_password: str):
        """Принимает новый пароль.
        Предполагает, что пользователь авторизован
        (только авторизованный пользователь может менять свой пароль).
        Изменяет пароль от учётной записи на указанный.

        Параметры
        ---------
        email : str
            Почта, которая привязана к той учётной записи, от которой надо поменять пароль
        old_password : str
            Старый пароль от учётной записи
        new_password : str
            Новый пароль от учётной записи
        """
        answer = self.sign_in(email, old_password)
        if answer is not None:
            return answer
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.put(url + 'users/change_password', data=new_password, headers=headers)
        if response.status_code != 204:
            return (response.status_code, response.json()['detail'])

    @connection_error_handler
    def reset_password(self, email: str):
        """Принимает почту, на котрую нужно отправить письмо с новым паролем."""
        response = requests.put(url + 'users/reset_password', data=email)
        if response.status_code != 204:
            return (response.status_code, response.json()['detail'])

    @connection_error_handler
    def change_email(self, old_email: str, password: str, new_email: str):
        """Изменяет почту от учтёной записи на указанную.
        
        Параметры
        ---------
        old_email : str
            Старая почта
        password : str
            Пароль от учётной записи
        new_email : str
            Новая почта
        """

        answer = self.sign_in(old_email, password)
        if answer is not None:
            return answer
        
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.put(url + 'users/change_email', data=new_email, headers=headers)
        if response.status_code != 204:
            return (response.status_code, response.json()['detail'])

    @connection_error_handler
    def add_card(self, data: dict): 
        """Привязывает карту к учётной записи.
        В словаре хранятся ключи:
        'cardholder_name': Большими латинскими буквами через знак нижнего подчёркивания _
        'card_number': Номер карты: 12 цифр
        'expiry_date': Дата истечения срока: два числа через знак слэша /
        'cvv': Код на обратной стороне, трехзначное число.
        """
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = response.post(url + 'users/config/addcard', json=data, headers=headers)
        if response.status_code != 204:
            return (response.status_code, response.json()['detail'])
    
    # -------------------- РАБОТА С МЕНЮ --------------------

    @connection_error_handler
    def get_pizzas_page(self, offset: int, limit: int):
        """Получает страницу пицц с сервера.
        
        Параметры
        ---------
        offset : int
            Сколько элементов нужно отсупить от начала таблицы
        limit : int
            Сколько элементов должно быть в странице

        Возвращает
        ----------
        page : list of dict
            Возвращает страницу (список) объектов пицц (словарей) вида

            {
                'id': int
                'name': str
                'description': str
                'price': float
            }
        """
        return pizzas[offset:offset+limit]
        params = {'limit' : limit, 'offset' : offset}
        response = requests.get(url + 'pizzas', params=params)
        if response.status_code == 200:
            return response.json()
        return (response.status_code, response.json()['detail'])
    
    @connection_error_handler
    def get_pizza_by_id(self, id : int):
        response = requests.get(url + f'pizzas/{id}')
        if response.status_code == 200:
            return response.json()
        return response.status_code

    # ------------------ РАБОТА С КОРЗИНОЙ ПОЛЬЗОВАТЕЛЯ -----------------

    @connection_error_handler
    def get_cart_items(self):
        """Получить содержимое своей корзины (без пагинации, так как размер корзины заведомо небольшой)"""
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = requests.get(url + 'carts', headers=headers)
        if response.status_code == 200:
            return response.json()
        return (response.status_code, response.json()['detail'])
    
    @connection_error_handler
    def add_item_to_cart(self, data: dict):
        """Принимает словарь в следующем формате:
        'pizza_id': Айди пиццы, которую нужно добавить в корзину
        'dough': Желаемое тесто, а именно 'classic' или 'thin'. По умолчанию должно быть 1
        'quantity': Количество штук пицц. По умолчанию должно быть 1
        'size': Размер пиццы, а именно 'small', 'medium', 'large' или 1, 2, 3. По умолчанию 1

        Добавляет пиццу в корзину
        """
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = requests.post(url + '/carts', json=data, headers=headers)
        return response.status_code
    
    def update_item_in_cart(self, data: dict):
        """Принимает словарь в следующем формате:
        'pizza_id': Айди пиццы, которая изменяется
        'item_id': Айди объекта корзины, который нужно изменить
        'dough': Желаемое тесто, а именно 'classic' или 'thin'. По умолчанию должно быть 1
        'quantity': Количество штук пицц. По умолчанию должно быть 1
        'size': Размер пиццы, а именно 'small', 'medium', 'large' или 1, 2, 3. По умолчанию 1

        Изменяет объект корзины.
        """
    
    # ------------------ РАБОТА С ЗАКАЗАМИ ------------------

    @connection_error_handler
    def create_order(self, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = requests.post(url + '/orders', json=data, headers=headers)
        if response.status_code == 200:
            return response.text # ссылка на оплату
        return response.status_code

    @connection_error_handler
    def get_orders(self, limit : int, offset : int):
        params = {'limit' : limit, 'offset' : offset}
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = requests.get(url + 'orders', headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return response.status_code

    @connection_error_handler
    def id_order(self, id : int):
        headers = {'Authorization': f'Bearer {self.__token}'}
        response = requests.get(url + f'orders/{id}', headers=headers)
        if response.status_code == 200:
            return response.json()
        return response.status_code
    
    @connection_error_handler
    def get_time(self, address : str):
        params = {'address' : address}
        response = requests.get(url + 'delivery/time', params=params)
        if response.status_code == 200:
            return response.text
        return response.status_code

    @connection_error_handler
    def new_item(self, id : int, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = requests.patch(url + f'carts/{id}',  json=data, headers=headers)
        return response.status_code

    @connection_error_handler
    def change_item(self, id : int, data):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = requests.put(url + f'carts/{id}', json=data, headers=headers)
        return response.status_code
    
    @connection_error_handler
    def delete_item(self, id : int):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.__token}'}
        response = requests.delete(url + f'carts/{id}', headers=headers)
        return response.status_code