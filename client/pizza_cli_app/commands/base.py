import curses
from typing import List, Iterator
import json


class Base:
    """Базовая команда"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self, session):
        raise NotImplementedError('You must implement the run() method!')

    def print_paged(self, loader: Iterator[List[str]]) -> None:
        """Разбивает список элементов на страницы и выводит их постранично.

        Параметры
        ---------
        elements: List[List[str]]
            Список элементов. Элемент - список из строк, который представляет собой обособленный элемент вывода.
            Например, каждый элемент меню пиццерии может представлено в виде списка ["название пиццы", "описание пиццы"].
        """
        def prepare_pages(new_elements: List[List[str]], max_rows: int, pages: List[List[str]]) -> List[List[str]]:
            buffer = pages.pop()
            for element in new_elements:
                if len(buffer) + len(element) >= max_rows:
                    pages.append(buffer)
                    buffer = element
                    continue

                buffer.extend(element)
            pages.append(buffer)

            return pages
    
    
        def load(loader):
            try:
                return next(loader)
            except StopIteration:
                return []
    
        HELP_TEXT = "Type n, p or q (next, prev or quit):"

        error_message = ''
        try:
            stdscr = curses.initscr()
            stdscr.refresh()  # Обновляем экран после инициализации

            # Создаем окно, в котором будет отображаться текст
            window = curses.newwin(curses.LINES, curses.COLS, 0, 0)

            # Определяем количество строк, которое может отображаться в окне
            max_rows = window.getmaxyx()[0] - 1

            # Подгружаем первую пачку элементов и формируем страницы
            new_elements = load(loader)
            pages = prepare_pages(new_elements, max_rows, [[]])
            text = '\n'.join(map(str, pages))
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
                elif key == ord('p') and cur > 0:
                    cur -= 1
                elif key == ord('n'):
                    if cur + 1 < len(pages):
                        cur += 1
                    else:
                        old_pages_len = len(pages)
                        new_elements = load(loader)
                        pages = prepare_pages(new_elements, max_rows, pages)
                        if len(pages) > old_pages_len:
                            cur += 1

                # Очищаем окно и отображаем новую страницу
                window.clear()
                for i, s in enumerate(pages[cur]):
                    window.addstr(i, 0, s)
                window.addstr(max_rows, 0, HELP_TEXT)

                # Обновляем экран
                window.refresh()

        except Exception as e:
            error_message += 'При постраничном выводе произошла неизвестная ошибка.\n'
            error_message += f"An error occurred: {e}\n"
        finally:
            # Завершаем работу с curses и восстанавливаем терминал
            curses.endwin()
            print(error_message, end='')