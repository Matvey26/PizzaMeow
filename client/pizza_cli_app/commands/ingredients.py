import curses

from .base import Base
from ..utils.print_format import print_paged


class Ingredients(Base):
    """Команда для вывода меню пиццы"""

    async def run(self):
        show_id = self.options.show_id
        limit = 20

        async def get_all_ingredients():
            offset = 0
            while (
                ingredients := await self.session.get_ingredients_page(
                    offset,
                    limit
                )
            ):
                if isinstance(ingredients, tuple):
                    raise Exception(ingredients[1])
                data = []
                for ingredient in ingredients:
                    rows = [
                        f"{ingredient['id']}. {ingredient['name']}." if show_id
                        else f"{ingredient['name']}",
                        f"description: {ingredient.get('description', '')}",
                        f"price: {ingredient['price']}"
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
                get_all_ingredients(),
                header=['Ингредиенты:', '++++++++++++++++++'],
                sep=['------------------']
            )
        except curses.error as e:
            print('При постраничном выводе произошла ошибка. '
                  'Возможно вы изменили размер терминала.')
            print(e)
        except Exception as e:
            print('Произошла неизвестная ошибка.')
            print(e)
