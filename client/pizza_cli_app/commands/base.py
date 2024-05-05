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

    def print_paged(self, loader: Iterator[List[str]], limit: int = 10**9, header: List[str] = [], footer: List[str] = [], sep: List[str] = []) -> None:
        """Разбивает список элементов на страницы и выводит их постранично.

        Параметры
        ---------
        loader: Iterator[List[str]]
            Генератор элементов. В генераторе каждый элемент должен быть представлен в виде списка строк для вывода
            Например, каждый элемент меню пиццерии может представлено в виде списка ["название пиццы", "описание пиццы"].
        limit: int
            Максимальное число элементов на странице
        header: List[str]
            Фиксированные строки, которые выводятся в верху экрана
        footer: List[str]
            Фиксированные строки, которые выводятся снизу экрана
        sep: List[str]
            Строки, которые используются как разделитель между элементами
        """

        HELP_TEXT = "Type n, p or q (next, prev or quit):"

        # Создаем окно, в котором будет отображаться текст
        stdscr = curses.initscr()
        stdscr.refresh()
        window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        MAX_ROWS = window.getmaxyx()[0]
        free_rows = MAX_ROWS - len(header) - len(footer) - 1  # минус 1, потому что учитываем HELP_TEXT (см. ниже)

        def extend_pages(new_elements: List[List[str]], pages: List[List[str]]) -> List[List[str]]:
            """Добавляет к текущим страницам новые элементы."""
            buffer = pages.pop()
            buffer_elements_count = buffer.pop()
            for element in new_elements:
                if not element:
                    continue
                if len(buffer) + len(element) + len(sep) >= free_rows or buffer_elements_count >= limit:
                    buffer.append(buffer_elements_count)
                    pages.append(buffer)
                    buffer = element
                    buffer_elements_count = 1
                    buffer.extend(sep)
                    continue
                
                buffer_elements_count += 1
                buffer.extend(element)
                buffer.extend(sep)
            buffer.append(buffer_elements_count)
            pages.append(buffer)

            return pages
    
        def load(loader):
            try:
                return next(loader)
            except StopIteration:
                return []
        
        def print_page(page):
            window.clear()
            i = 0
            for s in header:
                window.addstr(i, 0, s)
                i += 1
            for s in pages[cur]:
                if isinstance(s, int):
                    break
                window.addstr(i, 0, s)
                i += 1
            for s in footer:
                window.addstr(i, 0, s)
                i += 1
            window.addstr(MAX_ROWS - 1, 0, HELP_TEXT)
            window.refresh()
    
        error_message = ''
        try:
            # Подгружаем первую пачку элементов, формируем страницы и отображаем первую страницу
            pages = extend_pages(load(loader), [[0]])
            cur = 0  # номер текущей страницы

            # Отображаем первую страницу
            print_page(pages[0])

            # Слушаем клавиши
            while True:
                key = stdscr.getch()

                if key == ord('q'):
                    break
                if key == ord('p'):
                    cur = max(0, cur - 1)
                if key == ord('n'):
                    if cur + 1 >= len(pages) - 1:
                        pages = extend_pages(load(loader), pages)
                    cur = min(cur + 1, len(pages) - 1)

                # Отображаем новую страницу
                print_page(pages[cur])
        
        except Exception as e:
            curses.endwin()
            raise
        finally:
            curses.endwin()