import curses
from typing import List, Iterator
import itertools
import asyncio


class Base:
    """Базовая команда"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self, session):
        raise NotImplementedError('You must implement the run() method!')
    
    async def load_spinner(self, window: curses.window, y: int, x: int):
        """Отрисовывает строчку с загрузкой крутилкой в объекте окна window (библиотека curses)
        на позиции x, y (y - строка терминала, x - столбец терминала).
        """
        spinner = [
            '⠆ loading.  ',
            '⠃ loading.  ',
            '⠉ loading.  ',
            '⠘ loading.  ',
            '⠰ loading.  ',
            '⠤ loading.  ',
            '⠆ loading.. ',
            '⠃ loading.. ',
            '⠉ loading.. ',
            '⠘ loading.. ',
            '⠰ loading.. ',
            '⠤ loading.. ',
            '⠆ loading...',
            '⠃ loading...',
            '⠉ loading...',
            '⠘ loading...',
            '⠰ loading...',
            '⠤ loading...',
        ]
        for cur_char in itertools.cycle(spinner):
            window.refresh()
            window.addstr(y, x, cur_char)
            window.refresh()
            await asyncio.sleep(0.1)

    def print_paged(self, window: curses.window, loader: Iterator[List[str]], limit: int = 10**9, header: List[str] = [], footer: List[str] = [], sep: List[str] = []) -> None:
        """Разбивает список элементов на страницы и выводит их постранично.

        Параметры
        ---------
        window: curses.window
            Объект класса window модуля curses - окно, в котором будут отрисовываться страницы
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

        # Получаем размеры окна
        MAX_ROWS = window.getmaxyx()[0]
        free_rows = MAX_ROWS - len(header) - len(footer) - 1  # минус 1, потому что учитываем HELP_TEXT

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
        
        def print_all(page):
            window.clear()
            i = 0
            for s in header:
                window.addstr(i, 0, s)
                i += 1
            for s in page:
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
            print_all(pages[0])

            # Слушаем клавиши
            while True:
                key = window.getch()

                if key == ord('q'):
                    break
                if key == ord('p'):
                    cur = max(0, cur - 1)
                if key == ord('n'):
                    if cur + 1 >= len(pages) - 1:
                        pages = extend_pages(load(loader), pages)
                    cur = min(cur + 1, len(pages) - 1)

                # Отображаем новую страницу
                print_all(pages[cur])
        
        except Exception as e:
            curses.endwin()
            raise
        finally:
            curses.endwin()
    
    def print_scrolled(self, window: curses.window, rows: List[str], header: List[str] = [], footer: List[str] = [], sep: List[str] = []) -> None:
        HELP_TEXT = 'Используйте стрелки вверх/вниз. Нажмите Enter чтобы продолжить.'

        MAX_ROWS = window.getmaxyx()[0]
        FREE_ROWS = MAX_ROWS - len(header) - len(footer) - 1

        # На сколько строк уже пролистано
        offset = 0
        try:
            # Вывод строк
            def print_all():
                window.clear()
                i = 0
                for s in header:
                    window.addstr(i, 0, s)
                    i += 1
                for s1 in rows[offset:offset + FREE_ROWS]:
                    window.addstr(i, 0, s1)
                    i += 1
                    for s2 in sep:
                        window.addstr(i, 0, s2)
                        i += 1
                for s in footer:
                    window.addstr(i, 0, s)
                    i += 1
                window.addstr(MAX_ROWS - 1, 0, HELP_TEXT)
                window.refresh()
            
            print_all()

            # Обработка нажатий
            while True:
                key = window.getch()

                if key == 27 :
                    if window.getch() == 91:
                        k = window.getch()
                        if k == 66:  # стрелка вниз
                            offset = min(offset + 1, max(0, len(rows) - FREE_ROWS))
                        elif k == 65:  # стрелка вверх
                            offset = max(offset - 1, 0)
                elif key == 10:  # Enter
                    window.clear()
                    window.refresh()
                    return
                
                print_all()

        except Exception:
            curses.endwin()
            raise

    def print_choices(self, window: curses.window, choices: List[str], header: List[str] = [], footer: List[str] = [], sep: List[str] = []) -> int:
        """Разбивает список элементов на страницы и выводит их постранично.

        Параметры
        ---------
        window: curses.window
            Объект класса window модуля curses - окно, в котором всё будет отображаться
        choices: List[str]
            Список строк, каждая строка - отдельный выбор.
        header: List[str]
            Фиксированные строки, которые выводятся в верху экрана
        footer: List[str]
            Фиксированные строки, которые выводятся снизу экрана
        sep: List[str]
            Строки, которые используются как разделитель между элементами
        
        Возвращает
        ----------
        selected_choice: int
            Индекс выбранного элемента (0-индексация, относитеьлно списка choices)
        """

        HELP_TEXT = 'Используйте стрелки вверх/вниз. Нажмите Enter чтобы продолжить.'

        MAX_ROWS = window.getmaxyx()[0]
        FREE_ROWS = MAX_ROWS - len(header) - len(footer) - 1

        selected_choice = 0
        offset = 0
        try:
            # Вывод вариантов выбора
            def print_choices():
                window.clear()
                i = 0
                for s in header:
                    window.addstr(i, 0, s)
                    i += 1
                for choice_index, choice in enumerate(choices[offset:offset + FREE_ROWS]):
                    choice_index += offset
                    if choice_index == selected_choice:
                        window.addstr(i, 0, choice, curses.A_BOLD)
                    else:
                        window.addstr(i, 0, choice)
                    i += 1
                for s in footer:
                    window.addstr(i, 0, s)
                    i += 1
                window.addstr(MAX_ROWS - 1, 0, HELP_TEXT)
                window.refresh()

            print_choices()

            # Обрабатываем нажатия клавиш
            while True:
                key = window.getch()

                if key == 27:
                    if window.getch() == 91:
                        k = window.getch()
                        if k == 66:  # стрелка вниз
                            selected_choice = min(selected_choice + 1, len(choices))
                            if selected_choice >= offset + FREE_ROWS:
                                offset += 1
                        elif k == 65:  # стрелка вверх
                            selected_choice = max(selected_choice - 1, 0)
                            if selected_choice < offset:
                                offset -= 1
                if key == 10:
                    window.clear()
                    window.refresh()
                    return selected_choice
                print_choices()

        except Exception:
            curses.endwin()
            raise