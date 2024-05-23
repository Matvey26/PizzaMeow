from .base import Base
from ..utils.print_format import print_paged

import curses


class Orders(Base):
    async def run(self):
        show_id = self.options.show_id
        limit = self.options.limit
        active = self.options.active
        all = self.options.all
        completed = self.options.completed

        if all:
            active = True
            completed = True

        async def get_all_orders():
            offset = 0
            while (orders := await self.session.get_orders(
                limit, offset, active=active, completed=completed)
            ):
                if isinstance(orders, tuple):
                    raise Exception(' '.join(map(str, orders)))
                data = []
                for order in orders:
                    rows = []
                    first_row = f"ID: {order['id']}. " if show_id else ''
                    first_row += f"Статус: {order['status']}"
                    rows.append(first_row)
                    for order_item in order['order_items']:
                        ingredients_text = []
                        for ingredient, count in order_item['ingredients'].items():
                            ingredients_text.append(f'{ingredient}: {count}')
                        ingredients_text = "\n ".join(ingredients_text)
                        rows.append(f"итого: {order_item['total_price']}₽")
                        rows.append(f"{order_item['pizza_name']}, "
                                    f"{order_item['quantity']} шт.")
                        rows.append(f"    размер: {order_item['size']}")
                        rows.append(f"    тесто: {order_item['dough']}")
                        rows.append(f"    ингредиенты: {ingredients_text}")
                    data.append(rows)
                yield data
                offset += limit
        try:
            stdscr = curses.initscr()
            stdscr.refresh()
            window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

            await print_paged(
                window,
                get_all_orders(),
                limit=limit,
                header=['Заказы:', '++++++++++++++++++'],
                sep=['------------------']
            )
        except curses.error as e:
            curses.endwin()
            print('При постраничном выводе произошла ошибка. '
                  'Возможно вы изменили размер терминала.')
            print(e)
        except Exception as e:
            curses.endwin()
            print('Произошла ошибка.')
            print(e)
            raise
