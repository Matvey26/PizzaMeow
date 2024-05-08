from .base import Base
from ..api.api import Session
import curses
from typing import List


class Checkout(Base):
    """Создаёт заказ из собранной корзины."""
    def cart_information_screen(self, stdscr, cart: dict) -> None:
        # Подготовливаем окно.
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        try:
            # Подготавливаем строки для вывода
            rows = [f"Итоговая цена: {cart['total_price']}"]
            for i, item in enumerate(cart['cart_items']):
                line = f"{i}. {item['pizza_name']}, {item['quantity']} шт; "
                line += f"size: {item['size']}, dough: {item['dough']}"
                rows.append(line)

            
            # Выводим строки
            maxrows = window.getmaxyx()[0]
            offset = 0

            def print_page():
                window.clear()
                for i, row in enumerate(rows[offset:offset+maxrows - 1]):
                    window.addstr(i, 0, row)
                window.addstr(maxrows - 1, 0, 'Используйте стрелки вверх/вниз. Нажмите Enter чтобы продолжить.')
                window.refresh()
            
            print_page()

            # Обрабатываем нажатия
            while True:
                key = stdscr.getch()

                if key == 27 :
                    if stdscr.getch() == 91:
                        k = stdscr.getch()
                        if k == 66:  # стрелка вниз
                            offset = min(offset + 1, len(rows) - maxrows)
                        elif k == 65:  # стрелка вверх
                            offset = max(offset - 1, 0)
                elif key == 10:  # Enter
                    window.clear()
                    window.refresh()
                    return
                print_page()

        except Exception:
            curses.endwin()
            raise
    
    def choose_pickup_method_screen(self, stdscr):
        # Подготовливаем окно.
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

        try:
            choices = ["Самовывоз", "Доставка"]

            # Выводим варианты выбора
            selected_choice = 0

            def print_choices():
                window.clear()
                window.addstr(0, 0, 'Как будете забирать заказ?')
                for i, choice in enumerate(choices, 1):
                    if i - 1 == selected_choice:
                        window.addstr(i, 0, choice, curses.A_BOLD)
                    else:
                        window.addstr(i, 0, choice)
                window.refresh()
            print_choices()

            # Обрабатываем нажатия клавиш
            while True:
                key = stdscr.getch()

                if key == 27:
                    if stdscr.getch() == 91:
                        k = stdscr.getch()
                        if k == 66:  # стрелка вниз
                            selected_choice = min(1, selected_choice + 1)
                        elif k == 65:  # стрелка вверх
                            selected_choice = max(0, selected_choice - 1)
                if key == 10:
                    window.clear()
                    window.refresh()
                    return selected_choice
                print_choices()

        except Exception:
            curses.endwin()
            raise

    def run(self, session: Session):
        stdscr = curses.initscr()

        answer = session.get_cart_items()
        if isinstance(answer, tuple):
            print(answer[1])
        
        self.cart_information_screen(stdscr, answer)
        choice = self.choose_pickup_method_screen(stdscr)
        if choice:
            # Тут для доставки
            pass
        else:
            # Тут для самовывоза
            pass
    
        curses.endwin()