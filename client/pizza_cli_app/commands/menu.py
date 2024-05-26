import curses

from .base import Base
from ..utils.print_format import print_paged


class Menu(Base):
    """Команда для вывода меню пиццы"""

    async def run(self):
        show_id = self.options.show_id
        limit = 15
        with_preferences = self.options.with_preferences

        async def get_all_pizzas():
            offset = 0
            while (
                pizzas := await self.session.get_pizzas_page(
                    offset,
                    limit,
                    with_preferences
                )
            ):
                if isinstance(pizzas, tuple):
                    raise Exception(pizzas[1])
                data = []
                for pizza in pizzas:
                    rows = [
                        f"{pizza['id']}. {pizza['name']}." if show_id
                        else f"{pizza['name']}",
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

            await print_paged(
                window,
                get_all_pizzas(),
                header=['Меню:', '++++++++++++++++++'],
                sep=['------------------']
            )
        except curses.error as e:
            print('При постраничном выводе произошла ошибка. '
                  'Возможно вы изменили размер терминала.')
            print(e)
        except Exception as e:
            print('Произошла неизвестная ошибка.')
            print(e)
