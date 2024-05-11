import asyncio
from .base import Base
import curses


class Menu(Base):
    """Команда для вывода меню пиццы"""

    async def run(self):
        show_id = self.options.show_id
        limit = self.options.limit

        async def get_all_pizzas():
            offset = 0
            while (pizzas := await self.session.get_pizzas_page(offset, limit)):
                if isinstance(pizzas, tuple):
                    raise Exception(pizzas[1])
                data = []
                for pizza in pizzas:
                    rows = [
                        f"{pizza['id']}. {pizza['name']}." if show_id else f"{pizza['name']}",
                        f"description: {pizza.get('description', '')}",
                        f"price: {pizza['price']}"
                    ]
                    data.append(rows)
                yield data
                offset += limit

        try:
            stdscr = curses.initscr()
            stdscr.refresh()
            window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

            await self.print_paged(
                window,
                get_all_pizzas(),
                limit=limit,
                header=['Меню:', '++++++++++++++++++'],
                sep=['------------------']
            )
        except curses.error as e:
            print('При постраничном выводе произошла ошибка. Возможно вы изменили размер терминала.')
        except Exception as e:
            print('Произошла неизвестная ошибка.')
            print(e)
