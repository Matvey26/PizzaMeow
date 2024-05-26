import asyncio
import curses

from ..utils.print_format import load_spinner
from ..utils.print_format import print_paged
from ..utils.async_utils import aiter
from .base import Base
from .checkout import Checkout


class Repeat(Base):
    """Создаёт заказ из собранной корзины."""

    async def order_information_screen(
        self,
        stdscr: curses.window,
        order_id: int
    ) -> None:
        # Подготовливаем окно.
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        task_load = asyncio.create_task(load_spinner())
        task_get_order = asyncio.create_task(
            self.session.get_order_by_id(order_id)
        )

        order = await task_get_order
        task_load.cancel()

        if isinstance(order, tuple):
            raise RuntimeError(order[1])

        # Подготавливаем строки для вывода
        rows = [f"Итоговая цена: {order['total_price']}"]
        for i, item in enumerate(order['order_items']):
            line = f"{i}) {item['pizza_name']}, {item['quantity']} шт; "
            line += f"size: {item['size']}, dough: {item['dough']}"
            rows.append(line)

        # Выводим корзину
        print_paged(window, aiter([rows]))
        stdscr.clear()

    async def run(self):
        order_id = self.options.order_id

        stdscr = curses.initscr()
        stdscr.refresh()

        checkout_cmd = Checkout(self.options, self.session)

        try:
            await self.order_information_screen(stdscr, order_id)
            chosen_pickup_method = checkout_cmd.choose_pickup_method_screen(
                stdscr)

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

            address = await checkout_cmd.choose_address_screen(
                stdscr, search_addresses_function
            )
            time_interval = await checkout_cmd.choose_time_interval(
                stdscr, address, get_time_intervals_function
            )
            payment_method = \
                await checkout_cmd.choose_payment_method_screen(stdscr)
            payref = await self.session.repeat_order(
                order_id,
                {
                    'is_delivery': bool(chosen_pickup_method == 'Доставка'),
                    'address': address,
                    'time_interval': time_interval,
                    'payment_method': payment_method
                }
            )

            curses.endwin()
            if payref is not None:
                print('Ссылка для оплаты заказа:')
                print(payref)

        except Exception as e:
            curses.endwin()
            print(e)
            raise
        finally:
            curses.endwin()
