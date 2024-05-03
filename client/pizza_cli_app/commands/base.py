import curses
from typing import List


class Base:
    """Базовая команда"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self, session):
        raise NotImplementedError('You must implement the run() method!')

    def print_paged(self, elements: List[List[str]]) -> None:
        """Разбивает список элементов на страницы и выводит их постранично.

        Параметры
        ---------
        elements: List[List[str]]
            Список элементов. Элемент - список из строк, который представляет собой обособленный элемент вывода.
            Например, каждый элемент меню пиццерии может представлено в виде списка ["название пиццы", "описание пиццы"].
        """
        def prepare_pages(elements: List[List[str]], max_rows: int) -> List[List[str]]:
            pages = []
            buffer = []
            rest_row = max_rows
            for element in elements:
                if len(element) > rest_row:
                    pages.append(buffer)
                    buffer = element
                    rest_row = max_rows - len(element)
                    continue

                buffer.extend(element)
                rest_row -= len(element)
            pages.append(buffer)

            return pages

        HELP_TEXT = "Type n, p or q (next, prev or quit):"

        try:
            stdscr = curses.initscr()
            stdscr.refresh()  # Обновляем экран после инициализации

            # Создаем окно, в котором будет отображаться текст
            window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

            # Определяем количество строк, которое может отображаться в окне
            max_rows = window.getmaxyx()[0] - 1

            pages = prepare_pages(elements, max_rows)
            cur = 0  # номер текущей страницы

            # Отображаем первую страницу
            for i, s in enumerate(pages[cur]):
                window.addstr(i, 0, s)
            window.addstr(max_rows, 0, HELP_TEXT)

            # Обновляем экран
            window.refresh()

            while True:
                # Ожидаем нажатия клавиши
                key = stdscr.getch()

                # Выходим, если нажата клавиша 'q'
                if key == ord('q'):
                    break

                # Перемещаемся на следующую страницу
                elif key == ord('n') and cur + 1 < len(pages):
                    cur += 1
                elif key == ord('p') and cur > 0:
                    cur -= 1

                # Очищаем окно и отображаем новую страницу
                window.clear()
                for i, s in enumerate(pages[cur]):
                    window.addstr(i, 0, s)
                window.addstr(max_rows, 0, HELP_TEXT)

                # Обновляем экран
                window.refresh()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Завершаем работу с curses и восстанавливаем терминал
            curses.endwin()
            print('При постраничном выводе произошла неизвестная ошибка.')