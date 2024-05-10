import asyncio
import curses
import functools
import geopy
from typing import List

from .base import Base
from ..api.api import Session

import geopy.geocoders


geolocator = geopy.geocoders.Nominatim(user_agent='PizzaMeow_ClientApp')


async def search_addresses(address):
    loop = asyncio.get_running_loop()
    # Используем functools.partial() для передачи аргументов
    geocode_with_args = functools.partial(geolocator.geocode, address, exactly_one=False)
    locations = await loop.run_in_executor(None, geocode_with_args)
    if locations is None:
        return []
    return locations


class Checkout(Base):
    """Создаёт заказ из собранной корзины."""

    def cart_information_screen(self, stdscr: curses.window, cart: dict) -> None:
        # Подготовливаем окно.
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        # Подготавливаем строки для вывода
        rows = [f"Итоговая цена: {cart['total_price']}"]
        for i, item in enumerate(cart['cart_items']):
            line = f"{i}. {item['pizza_name']}, {item['quantity']} шт; "
            line += f"size: {item['size']}, dough: {item['dough']}"
            rows.append(line)
        
        self.print_scrolled(window, rows)
        stdscr.clear()
            
    
    def choose_pickup_method_screen(self, stdscr: curses.window) -> int:
        # Подготовливаем окно.
        stdscr.addstr(0, 0, 'Как будете забирать заказ?')
        stdscr.refresh()
        choice_window = curses.newwin(curses.LINES - 1, curses.COLS, 1, 0)
        choice_index = self.print_choices(choice_window, ['Доставка', 'Самовывоз'])
        stdscr.clear()
        return ['Доставка', 'Самовывоз'][choice_index]
    
    async def delivery_screen(self, stdscr: curses.window) -> str:
        stdscr.addstr(0, 0, 'Начните вводить свой адрес и нажмите Enter:')
        stdscr.refresh()
        input_window = curses.newwin(1, curses.COLS, 1, 0)
        input_window.move(0, 0)
        address = input_window.getstr()

        output_window = curses.newwin(curses.LINES - 2, curses.COLS, 2, 0)
        task_load = asyncio.create_task(self.load_spinner(output_window, 1, 0))
        task_search = asyncio.create_task(search_addresses(address))

        locations = await task_search
        task_load.cancel()

        addresses = [loc.address for loc in locations]
        output_window.clear()
        choice_index = self.print_choices(output_window, addresses)
        stdscr.clear()
        return addresses[choice_index]

    def run(self, session: Session):
        stdscr = curses.initscr()
        stdscr.refresh()

        answer = session.get_cart_items()
        if isinstance(answer, tuple):
            print(answer[1])
        
        self.cart_information_screen(stdscr, answer)
        choice = self.choose_pickup_method_screen(stdscr)
        if choice == 'Доставка':
            # Тут для доставки
            try:
                asyncio.run(self.delivery_screen(stdscr))
            except:
                curses.endwin()
                raise
        elif choice == 'Самовывоз':
            # Тут для самовывоза
            pass
    
        curses.endwin()