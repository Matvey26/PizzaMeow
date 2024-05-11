import asyncio
from .base import Base
import curses


class ShowOrders(Base):
    async def run(self):
        show_id = self.options.show_id
        limit = self.options.limit
        orders.add_argument('--limit', default=20, type=int, help='Максимум заказов на странице')
        activate = self.options.activate
        all = self.options.all
        completed = self.options.completed

        async def get_all_orders():
            offset = 0
            while (orders := await self.session.get_orders(limit, offset)):
                if isinstance(orders, tuple):
                    raise Exception(orders[1])
                data = []
                for order in orders:
                    rows = []
                    if show_id:
                        rows.append(f"Id order: {order['id']}.")
                    for order_item in order['order_items']:
                        if order_item['status'] is not 'done' and completed:
                            continue
                        if activate and order_item['status'] is 'done' or 'cancelled':
                            continue
                            rows.append(f"pizza_name: {order_item['pizza_name']}")
                            rows.append(f"total_price: {order_item['total_price']}")
                            rows.append(f"quantity: {order_item['quantity']}")
                            rows.append(f"size: {order_item['size']}")
                            rows.append(f"dough: {order_item['dough']}")
                            rows.append(f"status: {order_item['status']}")
                    data.append(rows)
                yield data
                offset += limit
        try:
            stdscr = curses.initscr()
            stdscr.refresh()
            window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

            await self.print_paged(
                window,
                get_all_orders(),
                limit=limit,
                header=['Заказы:', '++++++++++++++++++'],
                sep=['------------------']
            )
        except curses.error as e:
            print('При постраничном выводе произошла ошибка. Возможно вы изменили размер терминала.')
        except Exception as e:
            print('Произошла неизвестная ошибка.')
            print(e)

            