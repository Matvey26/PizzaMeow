"""Класс текущей сессии, предоставляющий удобный интерфейс взаимодействия клиента с сервером."""

import asyncio
import aiohttp
import functools
import geopy.geocoders
from .mock_data import *
import pathlib
import json


url = 'http://127.0.0.1:8000/api/'

geolocator = geopy.geocoders.Nominatim(user_agent='PizzaMeow_ClientApp')


def connection_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientConnectorError:
            return (-1, 'Ошибка соединения')

    return wrapper


class Session:
    def __init__(self):
        self._session = aiohttp.ClientSession()
        save_dir = pathlib.Path(__file__).parent.parent  # Папка pizza_cli_app
        save_path = save_dir / '.saved_token.json'
        save_path.touch()
        if save_path.stat().st_size == 0:
            with save_path.open('w') as file:
                json.dump({'token': ''}, file)
        with save_path.open('r') as file:
            self.__token = json.load(file).get('token', '')

    async def close(self):
        await self._session.close()

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
    async def sign_in(self, email: str, password: str):
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

        params = {'email': email, 'password': password}
        async with self._session.get(url + 'users/signin', params=params) as response:
            if response.status == 200:
                self.password = password
                self.email = email
                self.token = await response.text()
                return
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def sign_up(self, email: str, password: str):
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
        params = {'email': email, 'password': password}
        async with self._session.post(url + 'users/signup', json=params) as response:
            if response.status == 200:
                self.password = password
                self.email = email
                self.token = await response.text()
                return
            return (response.status, (await response.json())['detail'])

    def logout(self):
        self.token = ''

    @connection_error_handler
    async def config(self, data: dict):
        """Принимает словарь с данными, которые нужно обновить."""
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.token}'}
        async with self._session.patch(url + 'users/config', json=data, headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def change_password(self, email: str, old_password: str, new_password: str):
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
        answer = await self.sign_in(email, old_password)
        if answer is not None:
            return answer

        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.put(url + 'users/change_password', data=new_password, headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def reset_password(self, email: str):
        """Принимает почту, на котрую нужно отправить письмо с новым паролем."""
        async with self._session.put(url + 'users/reset_password', data=email) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def change_email(self, old_email: str, password: str, new_email: str):
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

        answer = await self.sign_in(old_email, password)
        if answer is not None:
            return answer

        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.put(url + 'users/change_email', data=new_email, headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def add_card(self, data: dict):
        """Привязывает карту к учётной записи.
        В словаре хранятся ключи:
        'cardholder_name': Большими латинскими буквами через знак нижнего подчёркивания _
        'card_number': Номер карты: 12 цифр
        'expiry_date': Дата истечения срока: два числа через знак слэша /
        'cvv': Код на обратной стороне, трехзначное число.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.post(url + 'users/config/addcard', json=data, headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    # -------------------- РАБОТА С МЕНЮ --------------------

    @connection_error_handler
    async def get_pizzas_page(self, offset: int, limit: int):
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
        # return pizzas[offset:offset+limit]
        params = {'limit': limit, 'offset': offset}
        async with self._session.get(url + 'pizzas', params=params) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_pizza_by_id(self, id: int):
        async with self._session.get(url + f'pizzas/{id}') as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    # ------------------ РАБОТА С КОРЗИНОЙ ПОЛЬЗОВАТЕЛЯ -----------------

    @connection_error_handler
    async def get_cart_items(self):
        """Получить содержимое своей корзины (без пагинации, так как размер корзины заведомо небольшой)
        Корзина представляет собой словарь вида

        {
            'id': int,  # id корзины
            'total_price': float,  # цена всей корзины
            'cart_items': list
        }

        где поле cart_items это список словарей объектов корзины вида

        {
            'id': int,  # уникальный ID элемента корзины
            'total_price': float  # цена за объект корзины (с учётом количества, размера, теста)
            'pizza_id': int,
            'pizza_name': str,
            'quantity': int,
            'size': str,  # а точнее enum: [small, medium, large]
            'dough': str  # а точнее enum: [thin, classic]
        }
        """
        # return cart
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.get(url + 'carts', headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def add_item_to_cart(self, data: dict):
        """Принимает словарь в следующем формате:
        'pizza_id': Айди пиццы, которую нужно добавить в корзину
        'quantity': Количество штук пицц. По умолчанию должно быть 1
        'size': Размер пиццы, а именно 'small', 'medium', 'large' или 1, 2, 3. По умолчанию 1
        'dough': Желаемое тесто, а именно 'classic' или 'thin'. По умолчанию должно быть 1

        Добавляет пиццу в корзину
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.post(url + 'carts', json=data, headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def update_item_in_cart(self, item_id: int, data: dict):
        """Изменяет объект корзины.

        Параметры
        ---------
        item_id: int
            Айди объекта корзины, который нужно изменить
        data: dict
            Данные для обновления. Словарь вида

            {
                'pizza_id': ID пиццы (на который нужно поменять)
                'dough': Другое тесто, а именно 'classic' или 'thin'. По умолчанию должно быть 1
                'quantity': Другое количество штук пицц. По умолчанию должно быть 1
                'size': Новый размер пиццы, а именно 'small', 'medium', 'large' или 1, 2, 3. По умолчанию 1
            }
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.patch(url + f'carts/{item_id}', json=data, headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def delete_item(self, item_id: int):
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.delete(url + f'carts/{item_id}', headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    # ------------------ РАБОТА С ЗАКАЗАМИ ------------------

    @connection_error_handler
    async def create_order(self, data):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.post(url + '/orders', json=data, headers=headers) as response:
            if response.status == 200:
                return await response.text()  # ссылка на оплату
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_orders(self, limit: int, offset: int):
        params = {'limit': limit, 'offset': offset}
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.get(url + 'orders', headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_order_by_id(self, id: int):
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.get(url + f'orders/{id}', headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    # ------------------ ВРЕМЯ И АДРЕСА ------------------

    @connection_error_handler
    async def get_time_delivery(self, address: str):
        """Возвращает список строк, в которых написаны интервалы времени,
        в которые может приехать курьер.
        Время в формате iso format!!!!
        (сервер сам учтёт время, которое потребуется на приготовление и сборку заказа).
        """
        # return [
        #     ['2024-05-15T10:00:15.310793+00:00', '2024-05-15T13:00:15.310793+00:00'],
        #     ['2024-05-15T13:00:15.310793+00:00', '2024-05-15T16:00:15.310793+00:00'],
        #     ['2024-05-15T16:00:15.310793+00:00', '2024-05-15T19:00:15.310793+00:00']
        # ]
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'address': address}
        async with self._session.get(url + 'time/delivery', headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_time_cooking(self, pizzeria_address: str) -> str:
        """Возвращает время в минутах, которое потребуется на приготовление заказа.
        (сервер сам посмотрит на корзину и оценит время её приготовления).
        """
        # return '25'
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'pizzeria_address': pizzeria_address}
        async with self._session.get(url + 'time/cooking', headers=headers, params=params) as response:
            if response.status == 200:
                return await response.text()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_pizzerias_addresses(self, limit: int = 10, address: str = None):
        """Если параметры не указаны, то возвращает все адреса пиццерий.
        Если указан параметр address, то вернёт 10 ближайших пиццерий.
        Если указаны параметры address и limit, то вернёт limit ближайших пиццерий.
        """
        # return [
        #     'Москва',
        #     'Санкт-Петербург',
        #     'Лондон'
        # ]
        params = {'address': address, 'count': limit}
        async with self._session.get(url + 'pizzeria/address', params=params) as response:
            if response.status == 200:
                return await response.text()
            return (response.status, (await response.json())['detail'])
    
    async def search_addresses(self, address):
        loop = asyncio.get_running_loop()
        # Используем functools.partial() для передачи аргументов
        geocode_with_args = functools.partial(
            geolocator.geocode,
            address, exactly_one=False
        )
        locations = await loop.run_in_executor(None, geocode_with_args)
        if locations is None:
            return []
        return locations

    async def is_valid_pickup_time(self, time: str) -> str:
        """Принимает строку с датой и временем в формате iso и проверяет, можно ли забрать заказ в это время.
        Ничего не возвращает, если всё хорошо. Если время не подходит, возвращает строку с объяснением."""
        return