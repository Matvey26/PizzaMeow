"""Класс текущей сессии, предоставляющий
интерфейс взаимодействия клиента с сервером."""

import asyncio
import aiohttp
import functools
from typing import List
import geopy.geocoders
import pathlib
import json


url = 'http://127.0.0.1:8000/api/'

geolocator = geopy.geocoders.Nominatim(user_agent='PizzaMeow_ClientApp')


def connection_error_handler(func):
    """Декоратор, обрабатывает ошибки соединения.
    Если происходит ошибка, функция возвращает кортеж (-1, 'Ошибка соединения')
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientConnectorError:
            return (-1, 'Ошибка соединения')

    return wrapper


class Session:
    """Класс текущей сессии. Предоставляет интерфейс
    для взаимодействия с сервером.
    Автоматически запоминает токен доступа,
    что позволяет единожды авторизоваться и
    длительное время пользоваться приложением.
    По окончании работы необходимо закрыть сессию с помощью метода close()
    """

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
        """Закрывает сессию. Необходимо вызывать
        после окончания работы с сессией."""
        await self._session.close()

    @property
    def token(self):
        """Возвращает сохранённый токен"""
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

    # ---------------- РАБОТА С УЧЁТНОЙ ЗАПИСЬЮ ПОЛЬЗОВАТЕЛЯ ------------------

    @connection_error_handler
    async def sign_in(self, email: str, password: str):
        """По данным регистрационным данным
        запрашивает у сервера токен доступа.

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
        async with self._session.get(url + 'users/signin', params=params) \
                as response:
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
            Почта, которая будет привязана к аккаунту
            (которая будет использоваться при входе)
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
        async with self._session.post(url + 'users/signup', json=params) \
                as response:
            if response.status == 200:
                self.password = password
                self.email = email
                self.token = await response.text()
                return
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def confirm_email(self, email: str):
        """Отправить письмо на почту с подтверждением учётной записи.

        Параметры
        ---------
        email: str
            Почта, на которую нужно отправить письмо

        Возвращает
        ----------
        ничего
            если письмо было успешно отправлено
        error: tuple
            если что-то пошло не так
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'email': email}
        async with self._session.get(url + 'users/confirm_email', params=params, headers=headers) \
                as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    def logout(self):
        """Очистить сохранённый токен. Теперь нужно повторно авторизоваться."""
        self.token = ''

    @connection_error_handler
    async def config(self, data: dict):
        """Принимает словарь с данными, которые нужно обновить.

        Параметры
        ---------
        data: dict
            Словарь с обновлёнными данными в следующем формате

            {
                'firstname': новое имя,
                'lastname': новая фамилия,
                'address': новый адрес,
                'phone': новый телефон
            }

            Указывать нужно только те параметры, которые надо обновить.

        Возвращает
        ----------
        ничего,
            если данные успешно обновлены
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.patch(
            url + 'users/config', json=data, headers=headers
        ) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def change_password(
        self,
        email: str,
        old_password: str,
        new_password: str
    ):
        """Изменяет пароль от учётной записи на указанный.

        Параметры
        ---------
        email: str
            Почта, которая привязана к той учётной записи,
            от которой надо поменять пароль
        old_password: str
            Старый пароль от учётной записи
        new_password: str
            Новый пароль от учётной записи
        """
        answer = await self.sign_in(email, old_password)
        if answer is not None:
            return answer

        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.put(
            url + 'users/change_password',
            data=new_password,
            headers=headers
        ) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def reset_password(self, email: str):
        """Отправляет сообщение с новыым паролем на указанную почту.
        Старый пароль сбрасывается и перестаёт работать.

        Параметры
        ---------
        email: str
            Почта, к которой был привязан аккаунт
            и на которую нужно отправить новый пароль.

        Возвращает
        ----------
        ничего,
            если сообщение было отправлено успешно
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """
        async with self._session.put(
                url + 'users/reset_password', data=email) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def change_email(
        self,
        old_email: str,
        password: str,
        new_email: str
    ):
        """Изменяет почту от учётной записи на указанную.

        Параметры
        ---------
        old_email: str
            Старая почта
        password: str
            Пароль от учётной записи
        new_email: str
            Новая почта

        Возвращает
        ----------
        ничего,
            если сообщение было отправлено успешно
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        answer = await self.sign_in(old_email, password)
        if answer is not None:
            return answer

        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.put(
            url + 'users/change_email',
            data=new_email,
            headers=headers
        ) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    # -------------------- РАБОТА С МЕНЮ --------------------

    @connection_error_handler
    async def get_pizzas_page(self, offset: int, limit: int):
        """Получить страницу меню пиццерии.

        Параметры
        ---------
        offset: int
            Сколько элементов нужно отсупить от начала таблицы
        limit: int
            Сколько элементов должно быть в странице

        Возвращает
        ----------
        page: list of dict
            Возвращает страницу (список) объектов пицц (словарей) вида

            {
                'id': int
                'name': str
                'description': str
                'price': float
            }

        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        params = {'limit': limit, 'offset': offset}
        async with self._session.get(
                url + 'pizzas', params=params) as response:
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
    async def get_cart(self):
        """Получить содержимое своей корзины (без пагинации,
        так как размер корзины заведомо небольшой)

        Корзина представляет собой словарь вида

        {
            'id': int,  # id корзины
            'total_price': float,  # цена всей корзины
            'cart_items': list
        }

        где поле cart_items это список словарей объектов корзины вида

        {
            'id': int,  # уникальный ID элемента корзины
            'total_price': float  # цена за объект корзины
                (с учётом количества, размера, теста)
            'pizza_id': int,
            'pizza_name': str,
            'quantity': int,
            'size': str,  # а точнее enum: [small, medium, large]
            'dough': str  # а точнее enum: [thin, classic]
        }

        Возвращает
        ----------
        cart: dict
            Корзина в указанном формате
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.get(
                url + 'carts', headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def add_item_to_cart(self, data: dict):
        """Добавляет пиццу в корзину

        Принимает словарь в следующем формате:



        Параметры
        ---------
        data: dict
            Словарь с добавляемым объектом в следующем формате:

            {
                'pizza_id': int,  # Айди пиццы, которую
                                    нужно добавить в корзину
                'quantity': int,  # Количество штук пицц.
                                    По умолчанию должно быть 1
                'size': str | int,  # Размер пиццы, а именно 'small', 'medium',
                                      'large' или 1, 2, 3. По умолчанию 1
                'dough': str | int,  # Желаемое тесто, а именно 'classic' или
                                       'thin'. По умолчанию должно быть 1
            }

        Возвращает
        ----------
        ничего,
            если сообщение было отправлено успешно
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.post(
                url + 'carts', json=data, headers=headers) as response:
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
                'dough': Другое тесто, а именно 'classic' или 'thin'.
                         По умолчанию должно быть 1
                'quantity': Другое количество штук пицц.
                            По умолчанию должно быть 1
                'size': Новый размер пиццы, а именно 'small', 'medium',
                        'large' или 1, 2, 3. По умолчанию 1
            }

        Возвращает
        ----------
        ничего,
            если сообщение было отправлено успешно
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.patch(
                url + f'carts/{item_id}',
                json=data, headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def delete_item(self, item_id: int):
        """Удалить предмет из корзины.

        Параметры
        ---------
        item_id: int
            ID объекта корзины, который нужно из неё убрать

        Возвращает
        ----------
        ничего,
            если сообщение было отправлено успешно
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.delete(
                url + f'carts/{item_id}', headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    # ------------------ РАБОТА С ЗАКАЗАМИ ------------------

    @connection_error_handler
    async def create_order(self, data: dict):
        """Создать новый заказ.

        Параметры
        ---------
        data: dict
            Словарь с информацией о заказе в формате:

            {
                'is_delivery': bool,  # Флаг, требуется ли доставлять заказ.
                'address': str,  # Если is_delivery = True, тогда это адрес,
                        куда нужно доставить. Иначе
                        адрес пиццерии, где нужно забрать заказ.
                'time_interval': List[str],  # Пара двух строк, в которых
                        записано время в формате iso
                        (можно пользоваться datetime.isoformat()).
                'payment_method': Enum('online', 'offline')  # Одна из двух
                        строк, которая говорит, как будет
                        производиться оплата заказа
            }

        Возвращает
        ----------
        payment_url: str
            Ссылку на оплату заказа, если
            payment_method = 'online' и запрос обработан успешно
        ничего
            Если payment_method = 'offline' и запрос обработан успешно
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.post(
                url + 'orders', json=data, headers=headers) as response:
            if response.status == 200:
                return await response.text()  # ссылка на оплату
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def repeat_order(self, order_id: int, data: dict):
        """Повторить заказ.

        Параметры
        ---------
        order_id: int
            Заказ, который нужно повторить
        data: dict
            Словарь с информацией о заказе в формате:

            {
                'is_delivery': bool,  # Флаг, требуется ли доставлять заказ.
                'address': str,  # Если is_delivery = True, тогда это адрес,
                        куда нужно доставить. Иначе
                        адрес пиццерии, где нужно забрать заказ.
                'time_interval': List[str],  # Пара двух строк, в которых
                        записано время в формате iso
                        (можно пользоваться datetime.isoformat()).
                'payment_method': Enum('online', 'offline')  # Одна из двух
                        строк, которая говорит, как будет
                        производиться оплата заказа
            }

        Возвращает
        ----------
        payment_url: str
            Ссылку на оплату заказа, если
            payment_method = 'online' и запрос обработан успешно
        ничего
            Если payment_method = 'offline' и запрос обработан успешно
        error: tuple
            кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        async with self._session.put(url + f'orders/{order_id}/repeat', json=data, headers=headers) as response:
            if response.status == 200:
                return await response.text()  # ссылка на оплату
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_orders(
            self, limit: int, offset: int, active=True, completed=False):
        """Получить страницу со всеми сделанными заказами.

        Параметры
        ---------
        limit: int
            Максимум заказов в странице
        offset: int
            Отступ от начала всех заказов (не глобально всех заказов,
            а относительно заказов пользователя)
        active: bool
            Флаг, active=True, возвращаются в том числе
            активные заказы (по умолчанию = True)
        completed: bool
            Флаг, completed=True, возвращаются в том числе
            завершённые заказы (по умолчанию = False)

        Возвращает
        ----------
        page: List[dict]
            Список словарей следующего формата:

            {
                'id': int,  # ID заказа
                'status': Enum('process', 'cooking',
                               'en_route', 'ready_to_pickup',
                               'done', 'cancelled'),
                'total_price': int,
                'delivery_price': int,
                'order_items': {
                    'total_price': int,  # итоговая цена за данную позицию
                    'pizza_name': str,  # название пиццы в этой позиции
                    'quantity': int,  # количество заказанных пицц
                    'size': Enum('small', 'medium', 'large'),
                    'dough': Enum('thin', 'classic')  # тесто заканных пицц
                }
            }
        error: tuple
            Кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        params = {
            'limit': limit,
            'offset': offset,
            'active': str(active).lower(),
            'completed': str(completed).lower()
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.get(
                url + 'orders', headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_order_by_id(self, order_id: int):
        """Возвращает заказ.

        Параметры
        order_id: int
            ID заказа, который нужно вернуть

        Возвращает
        ----------
        order: dict
            Словарь следующего формата

            {
                'id': int,  # ID заказа
                'status': Enum('process', 'cooking',
                               'en_route', 'ready_to_pickup',
                               'done', 'cancelled'),
                'total_price': int,
                'delivery_price': int,
                'order_items': {
                    'total_price': int,  # итоговая цена за данную позицию
                    'pizza_name': str,  # название пиццы в этой позиции
                    'quantity': int,  # количество заказанных пицц
                    'size': Enum('small', 'medium', 'large'),  # размер пицц
                    'dough': Enum('thin', 'classic')  # тесто заканных пицц
                }
            }
        error: tuple
            Кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.get(
                url + f'orders/{order_id}', headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def cancel_order(self, order_id: int):
        headers = {'Authorization': f'Bearer {self.token}'}
        async with self._session.put(
                url + f'orders/{order_id}/cancel',
                headers=headers) as response:
            if response.status != 204:
                return (response.status, (await response.json())['detail'])

    # ------------------ ВРЕМЯ И АДРЕСА ------------------

    @connection_error_handler
    async def get_time_delivery(self, address: str) -> List[List[str]]:
        """Получить список интервалов времени, в которые может приехать курьер.

        Параметры
        ---------
        address: str
            Адрес, куда нужно доставить заказ.
            Сервер сам учтёт время на приготовление заказа.

        Возвращает
        ----------
        time_intervals: List[List[str]]
            Список интервалов времени, в которые может приехать курьер.
            Список состоит из пар строк, которые являются временем
            в формате iso (можно воспользоваться datetime.isoformat()).
        error: tuple
            Кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'address': address}
        async with self._session.get(
                url + 'time/delivery',
                headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_time_cooking(self, pizzeria_address: str) -> List[List[str]]:
        """Получить список интервалов времени, в которые можно забрать заказ.

        Параметры
        ---------
        address: str
            Адрес пиццерии, где пользователь хочет забрать заказ.
            Сервер сам учтёт время на приготовление заказа.

        Возвращает
        ----------
        time_intervals: List[List[str]]
            Список интервалов времени, в которые можно забрать заказ
            Список состоит из пар строк, которые являются временем
            в формате iso (можно воспользоваться datetime.isoformat()).
        error: tuple
            Кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'pizzeria_address': pizzeria_address}
        async with self._session.get(
                url + 'time/cooking',
                headers=headers, params=params) as response:
            if response.status == 200:
                return await response.text()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def get_pizzerias_addresses(self, address: str = None):
        """Если параметры не указаны, то возвращает все адреса пиццерий.
        Если указан параметр address, то отсортирует по отдалению пиццерий

        Получить адреса пиццерий

        Параметры
        ---------
        address: str
            Необязательный параметр. Если указан, то адреса
            пиццерий отсортируются в порядке удаления от этого адреса

        Возвращает
        ----------
        pizzeria_addresses: List[str]
            Адреса пиццерий
        error: tuple
            Кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        params = {'address': address}
        async with self._session.get(
                url + 'pizzeria/address', params=params) as response:
            if response.status == 200:
                return await response.json()
            return (response.status, (await response.json())['detail'])

    @connection_error_handler
    async def search_addresses(self, address: str):
        """Получить список адресов, наиболее похожий на указанный

        Параметры
        ---------
        address: str
            Адрес, который будет геокодирован и для которого
            будут найдены наиболее релевантные адреса

        Возвращает
        ----------
        addresses: List[str]
            Список адресов, похожих на указанный
        error: tuple
            Кортеж вида (код ошибки, сообщение ошибки),
            если что-то пошло не так
        """

        loop = asyncio.get_running_loop()
        geocode_with_args = functools.partial(
            geolocator.geocode,
            address, exactly_one=False
        )
        locations = await loop.run_in_executor(None, geocode_with_args)
        if locations is None:
            return []
        return [loc.address for loc in locations]
