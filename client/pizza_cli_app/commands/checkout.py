import asyncio
import curses
import datetime
from typing import List

from .base import Base


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
            choice_window,
            choices
        )
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
            task_load = asyncio.create_task(
                self.load_spinner(output_window, 0, 0))
            # Делаем запрос к картам
            task_search = asyncio.create_task(
                self.session.search_addresses(address))

            locations = await task_search
            task_load.cancel()

            addresses = ['Повторить ввод'] + \
                [loc.address for loc in locations]
            output_window.clear()

            # Выводим адреса, чтобы пользователь выбрал нужный и получаем ответ от него
            choice_index = self.print_choices(output_window, addresses)

            # Даём человеку ввести ещё раз, если он не нашёл своего адреса
            if choice_index == 0:
                input_window.clear()
                output_window.clear()
                continue

            return addresses[choice_index]

    async def choose_delivery_time_screen(self, stdscr: curses.window, address: str) -> List[str]:
        # Подготавливаем окно
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        # Получаем интервалы времени
        task_load = asyncio.create_task(self.load_spinner(window, 0, 0))
        task_get_time_delivery = asyncio.create_task(
            self.session.get_time_delivery(address)
        )
        # time_intervals хранит пары строк, которые представляют собой объект datetime в iso формате в часовом поясе UTC
        time_intervals = await task_get_time_delivery
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
        choice_index = self.print_choices(window, formated_time_intervals)
        stdscr.clear()

        # Однако выбор потом нужно перевести обратно в универсальный строчный формат

        return time_intervals[choice_index]

    async def choose_pickup_address_screen(self, stdscr: curses.window) -> str:
        # Подготавливаем окно
        stdscr.addstr(0, 0, 'Начните вводить адрес пиццерии и нажмите Enter:')
        stdscr.refresh()
        input_window = curses.newwin(1, curses.COLS, 1, 0)

        while True:
            # Устанавливаем курсор в начало терминала и ожидаем ввод адреса
            input_window.move(0, 0)
            approximate_address = input_window.getstr().decode().strip()

            # Подготавливаем окно для вывода адресов
            output_window = curses.newwin(curses.LINES - 2, curses.COLS, 2, 0)

            # Запускаем загрузку-крутилку
            task_load = asyncio.create_task(
                self.load_spinner(output_window, 0, 0)
            )
            # Делаем запрос к серверу
            task_get_pizzerias_addresses = asyncio.create_task(
                self.session.get_pizzerias_addresses()
            )

            pizzerias_addresses = await task_get_pizzerias_addresses
            task_load.cancel()

            if isinstance(pizzerias_addresses, tuple):
                raise RuntimeError(pizzerias_addresses[1])

            pizzerias_addresses = ['Повторить ввод'] + pizzerias_addresses
            output_window.clear()

            # Выводим адреса, чтобы пользователь выбрал нужный и получаем ответ от него
            choice_index = self.print_choices(
                output_window,
                pizzerias_addresses
            )

            # Даём человеку ввести ещё раз, если он не нашёл своего адреса
            if choice_index == 0:
                input_window.clear()
                output_window.clear()
                continue

            return pizzerias_addresses[choice_index]

    async def choose_pickup_time_screen(self, stdscr: curses.window, pizzeria_address: str) -> str:
        stdscr.addstr(
            0, 0, 'Введите желаемое время в формате "дд.мм.гггг чч:мм" и нажмите Enter:')
        stdscr.refresh()
        input_window = curses.newwin(1, curses.COLS, 2, 0)
        output_window = curses.newwin(curses.LINES - 3, curses.COLS, 3, 0)

        task_load = asyncio.create_task(self.load_spinner())
        task_get_time_cooking = asyncio.create_task(
            self.session.get_time_cooking()
        )

        minutes_to_cooking = await task_get_time_cooking
        task_load.cancel()

        # TODO: добавить провеку на isinstance(tuple)

        time_text = ''
        if minutes_to_cooking >= 60:
            time_text = f"{minutes_to_cooking // 60} ч. {minutes_to_cooking % 60} мин."
        else:
            time_text = f"{minutes_to_cooking % 60} мин."
        stdscr.addstr(1, 0, f"Заказ будет готовиться {time_text}")

        time_format = '%d.%m.%Y %H:%M'
        while True:
            input_window.move(0, 0)
            desired_time = input_window.getstr()

            dt_utc_now = datetime.datetime.now(datetime.timezone.utc)
            dt_loc_now = datetime.datetime.now()

            try:
                dt_desired_time = datetime.datetime.strptime(
                    desired_time, time_format)
            except ValueError:
                input_window.clear()
                output_window.clear()
                output_window.addstr(0, 0, 'Неправильный формат ввода')
                input_window.refresh()
                output_window.refresh()
                continue

            if (dt_desired_time - dt_loc_now).min < minutes_to_cooking:
                input_window.clear()
                output_window.clear()
                output_window.addstr(0, 0, 'Нельзя забрать заказ раньше')
                input_window.refresh()
                output_window.refresh()
                continue

            dt_utc_desired_time = dt_utc_now + (dt_desired_time - dt_loc_now)

            task_load = asyncio.create_task(self.load_spinner())
            task_is_valid_pickup_time = asyncio.create_task(
                self.session.is_valid_pickup_time(dt_utc_desired_time)
            )

            # TODO: я тут закончил

    async def run(self):
        stdscr = curses.initscr()
        stdscr.refresh()

        try:
            await self.cart_information_screen(stdscr)
            chosen_pickup_method = self.choose_pickup_method_screen(stdscr)

            chosen_address = ''
            chosen_time_interval = ''

            if chosen_pickup_method == 'Доставка':
                chosen_address = await self.choose_delivery_address_screen(stdscr)
                chosen_time_interval = await self.choose_delivery_time_screen(stdscr, chosen_address)

            elif chosen_pickup_method == 'Самовывоз':
                chosen_pizzeria = await self.choose_pickup_address_screen(stdscr)

        except Exception as e:
            curses.endwin()
            print(e)
        finally:
            curses.endwin()
