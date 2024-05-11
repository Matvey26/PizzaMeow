from .base import Base
import curses


class Cart(Base):
    """Выводит корзину пользователя"""

    def run(self):
        show_id = self.options.show_id
        answer = self.session.get_cart_items()

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
            if show_id:
                element.append(f"ID элемента корзины: {item['id']}")
            element.append(f"Цена - {item['total_price']}")
            element.append(f"Название пиццы - {item['pizza_name']}")
            element.append(f"Количество - {item['quantity']}")
            element.append(f"Размер пиццы - {item['size']}")
            element.append(f"Тип теста - {item['dough']}\n")
            elements.append(element)

        stdscr = curses.initscr()
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.print_paged(window, iter([elements]), header=header, sep=sep)
