import asyncio
import curses

from ..utils.async_utils import aiter
from ..utils.print_format import print_paged, load_spinner
from .base import Base


class Cart(Base):
    """Выводит корзину пользователя"""

    async def run(self):
        show_id = self.options.show_id

        task_load = asyncio.create_task(load_spinner())
        task_get_cart_items = asyncio.create_task(
            self.session.get_cart()
        )

        answer = await task_get_cart_items
        task_load.cancel()

        if isinstance(answer, tuple):
            print(answer[1])
            return

        header = [
            f"Цена корзины: {answer['total_price']}",
            '+++++++++++++++++++++++++++++'
        ]
        sep = [
            '-----------------------------'
        ]
        elements = []
        for item in answer['cart_items']:
            element = []
            ingredients_text = []
            for ingredient in item['ingredients']:
                ingredients_text.append(f'{ingredient["id"]}: '
                                        f'{ingredient["quantity"]}')
            ingredients_text = ", ".join(ingredients_text)
            if show_id:
                element.append(f"ID элемента корзины: {item['id']}")
            element.append(f"Цена - {item['total_price']}")
            element.append(f"Название пиццы - {item['pizza_name']}")
            element.append(f"Количество - {item['quantity']}")
            element.append(f"Размер пиццы - {item['size']}")
            element.append(f"Тип теста - {item['dough']}\n")
            element.append(f"Ингредиенты - {ingredients_text}\n")
            elements.append(element)

        stdscr = curses.initscr()
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        await print_paged(
            window,
            aiter([elements]),
            header=header,
            sep=sep
        )
