import asyncio
import curses
import functools
from fuzzywuzzy import fuzz
import geopy
from typing import List

from .base import Base
from ..api.api import Session

import geopy.geocoders


geolocator = geopy.geocoders.Nominatim(user_agent='PizzaMeow_ClientApp')


async def search_addresses(address):
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


def sort_strings_by_similarity(pattern: str, strings: List[str]):
    """
    Сортирует список строк strings в порядке убывания их схожести со строкой pattern.
    """
    # Используем функцию fuzz.ratio() для сравнения схожести строк.
    # key=lambda x: fuzz.ratio(s, x) - компаратор
    # На первом месте должны быть наиболее подходящие, поэтому reverse=True.
    return sorted(strings, key=lambda x: fuzz.ratio(pattern, x), reverse=True)


class Checkout(Base):
    """Создаёт заказ из собранной корзины."""

    async def cart_information_screen(self, stdscr: curses.window) -> None:
        # Подготовливаем окно.
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        task_load = asyncio.create_task(self.load_spinner())
        task_get_cart_items = asyncio.create_task(
            self.session.get_cart_items()
        )

        cart = await task_get_cart_items
        task_load.cancel()

        if isinstance(cart, tuple):
            raise RuntimeError(cart[1])

        # Подготавливаем строки для вывода
        rows = [f"Итоговая цена: {cart['total_price']}"]
        for i, item in enumerate(cart['cart_items']):
            line = f"{i}) {item['pizza_name']}, {item['quantity']} шт; "
            line += f"size: {item['size']}, dough: {item['dough']}"
            rows.append(line)

        # Выводим корзину
        self.print_scrolled(window, rows)
        stdscr.clear()

    def choose_pickup_method_screen(self, stdscr: curses.window) -> int:
        # Подготовливаем окно.
        stdscr.addstr(0, 0, 'Как будете забирать заказ?')
        stdscr.refresh()
        choice_window = curses.newwin(curses.LINES - 1, curses.COLS, 1, 0)

        # Выводим список выборов и получаем ответ пользователя
        choices = ['Доставка', 'Самовывоз']
        choice_index = self.print_choices(
            choice_window, choices)
        stdscr.clear()

        return choices[choice_index]

    async def choose_delivery_address_screen(self, stdscr: curses.window) -> str:
        # Подготавливаем окно
        stdscr.addstr(0, 0, 'Начните вводить свой адрес и нажмите Enter:')
        stdscr.refresh()
        input_window = curses.newwin(1, curses.COLS, 1, 0)

        while True:
            # Устанавливаем курсор в начало терминала и ожидаем ввод адреса
            input_window.move(0, 0)
            address = input_window.getstr().decode().strip()

            # Подготавливаем окно для вывода адресов
            output_window = curses.newwin(curses.LINES - 2, curses.COLS, 2, 0)

            # Запускаем загрузку-крутилку
            task_load = asyncio.create_task(self.load_spinner(output_window, 0, 0))
            # Делаем запрос к картам
            task_search = asyncio.create_task(search_addresses(address))

            locations = await task_search
            task_load.cancel()

            addresses = [loc.address for loc in locations[:25]] + ['Здесь нет моего адреса']
            output_window.clear()

            # Выводим адреса, чтобы пользователь выбрал нужный и получаем ответ от него
            choice_index = self.print_choices(output_window, addresses)

            # Даём человеку ввести ещё раз, если он не нашёл своего адреса
            if choice_index == len(addresses) - 1:
                input_window.clear()
                output_window.clear()
                continue

            return addresses[choice_index]

    async def choose_delivery_time_screen(self, stdscr: curses.window, address: str) -> str:
        # Подготавливаем окно
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        # Получаем интервалы времени
        task_load = asyncio.create_task(self.load_spinner(window, 0, 0))
        task_get_time_delivery = asyncio.create_task(
            self.session.get_time_delivery(address)
        )
        time_intervals = await task_get_time_delivery
        task_load.cancel()

        if isinstance(time_intervals, tuple):
            raise RuntimeError(time_intervals[1])

        # TODO: Добавить человеческий вывод времени (сначала перевод в datetime, а потом в удобный строчный формат)

        # Предлагаем пользователю выбрать подходящий интервал времени
        choice_index = self.print_choices(window, time_intervals)
        stdscr.clear()

        # Однако выбор потом нужно перевести обратно в универсальный строчный формат

        return time_intervals[choice_index]

    # TODO: то же самое, что и в delivery_screen. Да и вообще доделать
    async def pickup_screen(self, stdscr: curses.window) -> str:
        # Подготавливаем окно
        stdscr.addstr(0, 0, 'Выберите адрес пиццерии или начните вводить его и нажмите Enter:')
        stdscr.refresh()

        task_load = asyncio.create_task(self.load_spinner())
        task_get_pizzerias_addresses = asyncio.create_task(
            self.session.get_pizzerias_addresses()
        )

        addresses = await task_get_pizzerias_addresses
        task_load.cancel()

        if isinstance(addresses, tuple):
            raise RuntimeError(addresses[1])

    async def run(self):
        stdscr = curses.initscr()
        stdscr.refresh()

        try:
            await self.cart_information_screen(stdscr)
            chosen_pickup_method = self.choose_pickup_method_screen(stdscr)

            chosen_address = ''
            chosen_time_interval = ''

            if chosen_pickup_method == 'Доставка':
                try:
                    chosen_address = await self.choose_delivery_address_screen(stdscr)
                    chosen_time_interval = await self.choose_delivery_time_screen(stdscr, chosen_address)
                except:
                    curses.endwin()
                    raise

            elif chosen_pickup_method == 'Самовывоз':
                self.pickup_screen(stdscr)

        except Exception as e:
            curses.endwin()
            print(e)
            raise
        finally:
            curses.endwin()
