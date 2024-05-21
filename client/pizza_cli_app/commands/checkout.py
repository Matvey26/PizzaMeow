import asyncio
import curses
import datetime
from typing import List
from ..utils.print_format import load_spinner
from ..utils.print_format import print_choices
from ..utils.print_format import print_scrolled

from .base import Base


class Checkout(Base):
    """Создаёт заказ из собранной корзины."""

    async def cart_information_screen(self, stdscr: curses.window) -> None:
        # Подготовливаем окно.
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        task_load = asyncio.create_task(load_spinner())
        task_get_cart_items = asyncio.create_task(
            self.session.get_cart()
        )

        cart = await task_get_cart_items
        task_load.cancel()

        if isinstance(cart, tuple):
            raise RuntimeError(cart[1])

        if len(cart['cart_items']) == 0:
            raise RuntimeError('Ваша корзина пуста')

        # Подготавливаем строки для вывода
        rows = [f"Итоговая цена: {cart['total_price']}"]
        for i, item in enumerate(cart['cart_items']):
            line = f"{i}) {item['pizza_name']}, {item['quantity']} шт; "
            line += f"size: {item['size']}, dough: {item['dough']}"
            rows.append(line)

        # Выводим корзину
        print_scrolled(window, rows)
        stdscr.clear()

    def choose_pickup_method_screen(self, stdscr: curses.window) -> int:
        # Подготовливаем окно.
        stdscr.addstr(0, 0, 'Как будете забирать заказ?')
        stdscr.refresh()
        choice_window = curses.newwin(curses.LINES - 1, curses.COLS, 1, 0)

        # Выводим список выборов и получаем ответ пользователя
        choices = ['Доставка', 'Самовывоз']
        choice_index = print_choices(
            choice_window,
            choices
        )

        stdscr.clear()
        return choices[choice_index]

    async def choose_address_screen(
        self,
        stdscr: curses.window,
        search_addresses_func
    ) -> str:

        # Подготавливаем окно
        stdscr.addstr(0, 0, 'Начните вводить адрес и нажмите Enter:')
        stdscr.refresh()
        input_window = curses.newwin(1, curses.COLS, 1, 0)

        while True:
            # Устанавливаем курсор в начало терминала и ожидаем ввод адреса
            input_window.move(0, 0)
            address = input_window.getstr().decode().strip()

            # Подготавливаем окно для вывода адресов
            output_window = curses.newwin(curses.LINES - 2, curses.COLS, 2, 0)

            # Запускаем загрузку-крутилку
            task_load = asyncio.create_task(
                load_spinner(output_window, 0, 0))
            # Делаем запрос к серверу для получения адресов
            task_search = asyncio.create_task(search_addresses_func(address))

            addresses = await task_search
            task_load.cancel()

            if isinstance(addresses, tuple):
                raise RuntimeError(addresses[1])

            addresses = ['Повторить ввод'] + addresses
            output_window.clear()

            # Выводим адреса, чтобы пользователь выбрал нужный
            # и получаем ответ от него
            choice_index = print_choices(output_window, addresses)

            # Даём человеку ввести ещё раз, если он не нашёл своего адреса
            if choice_index == 0:
                input_window.clear()
                output_window.clear()
                continue

            stdscr.clear()
            return addresses[choice_index]

    async def choose_time_interval(
        self,
        stdscr: curses.window,
        address: str,
        get_time_intervals_func
    ) -> List[str]:
        # Подготавливаем окно
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        # Получаем интервалы времени
        task_load = asyncio.create_task(load_spinner(window, 0, 0))
        task_get_time_intervals = asyncio.create_task(
            get_time_intervals_func(address)
        )
        # time_intervals хранит пары строк, которые представляют собой
        # объект datetime в iso формате в часовом поясе UTC
        time_intervals = await task_get_time_intervals
        task_load.cancel()

        if isinstance(time_intervals, tuple):
            raise RuntimeError(time_intervals[1])

        # --- Переводим интервалы в человеческий вид ---
        formated_time_intervals = []

        # вычисляем разницу между utc и локальным часовым поясом
        hour_dif = datetime.datetime.now().hour - \
            datetime.datetime.now(datetime.timezone.utc).hour
        td_hour_dif = datetime.timedelta(hours=hour_dif)
        for time_interval in time_intervals:
            start, end = time_interval

            d_start = datetime.datetime.fromisoformat(start) + td_hour_dif
            d_end = datetime.datetime.fromisoformat(end) + td_hour_dif

            if (d_end - d_start).days < 1:
                pref = d_start.strftime('%d %B')
                f_start = datetime.datetime.strftime(d_start, '%H:%M')
                f_end = datetime.datetime.strftime(d_end, '%H:%M')
                formated_time_intervals.append(f"{pref}, {f_start} - {f_end}")
            else:
                f_start = datetime.datetime.strftime(d_start, '%d %B, %H:%M')
                f_end = datetime.datetime.strftime(d_end, '%d %B, %H:%M')
                formated_time_intervals.append(f"{f_start} - {f_end}")

        # Предлагаем пользователю выбрать подходящий интервал времени
        choice_index = print_choices(window, formated_time_intervals)
        stdscr.clear()

        # Однако выбор потом нужно перевести обратно
        # в универсальный строчный формат
        stdscr.clear()
        return time_intervals[choice_index]

    async def choose_payment_method_screen(self, stdscr: curses.window):
        # Подготовливаем окно.
        stdscr.addstr(0, 0, 'Как будете оплачивать заказ?')
        stdscr.refresh()
        choice_window = curses.newwin(curses.LINES - 1, curses.COLS, 1, 0)

        # Выводим список выборов и получаем ответ пользователя
        choices = ['online', 'offline']
        choice_index = print_choices(
            choice_window,
            choices
        )

        stdscr.clear()
        return choices[choice_index]

    async def run(self):
        stdscr = curses.initscr()
        stdscr.refresh()

        try:
            await self.cart_information_screen(stdscr)
            chosen_pickup_method = self.choose_pickup_method_screen(stdscr)

            search_addresses_function = None
            get_time_intervals_function = None

            if chosen_pickup_method == 'Доставка':
                search_addresses_function = self.session.search_addresses
                get_time_intervals_function = self.session.get_time_delivery

            elif chosen_pickup_method == 'Самовывоз':
                search_addresses_function = (
                    self.session.get_pizzerias_addresses
                )
                get_time_intervals_function = self.session.get_time_cooking

            address = await self.choose_address_screen(
                stdscr, search_addresses_function
            )
            time_interval = await self.choose_time_interval(
                stdscr, address, get_time_intervals_function
            )
            payment_method = await self.choose_payment_method_screen(stdscr)
            payref = await self.session.create_order({
                'is_delivery': bool(chosen_pickup_method == 'Доставка'),
                'address': address,
                'time_interval': time_interval,
                'payment_method': payment_method
            })

            curses.endwin()
            if payref is not None:
                print('Ссылка для оплаты заказа:')
                print(payref)

        except Exception as e:
            curses.endwin()
            print(e)

        curses.endwin()
