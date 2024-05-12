import asyncio
from .base import Base
import curses


class Orders(Base):
    async def run(self):
        show_id = self.options.show_id
        limit = self.options.limit
        active = self.options.active
        all = self.options.all
        completed = self.options.completed

        order_status_filter = []
        if active or all:
            order_status_filter.extend([
                'process',
                'cooking',
                'en_route',
                'ready_to_pickup',
            ])
        if completed or all:
            order_status_filter.extend([
                'done',
                'cancelled'
            ])

        async def get_all_orders():
            offset = 0
            while (orders := await self.session.get_orders(limit, offset)):
                if isinstance(orders, tuple):
                    raise Exception(' '.join(map(str, orders)))
                data = []
                for order in orders:
                    rows = []
                    first_row = f"ID: {order['id']}. " if show_id else ''
                    first_row += f"Статус: {order['status']}"
                    rows.append(first_row)
                    for order_item in order['order_items']:
                        if order_item['status'] in order_status_filter:
                            rows.append(f"итого: {order_item['total_price']}₽")
                            rows.append(f"{order_item['pizza_name']}, {order_item['quantity']} шт.")
                            rows.append(f"\tразмер: {order_item['size']}")
                            rows.append(f"\tтесто: {order_item['dough']}")
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
            print('Может быть, вы забыли авторизоваться?')
            print(e)