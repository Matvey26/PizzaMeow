import curses
from typing import List, AsyncIterator
import itertools
import asyncio
import sys


PAGED_HELP = 'Use keys w, a, s, d to navigates. Prees q to quit:'
CHOICES_HELP = 'Use keys w, s to scrolling. Press Enter to continue.'


async def load_spinner(
    window: curses.window = None,
    y: int = 0,
    x: int = 0
):
    """Отрисовывает строчку с загрузкой крутилкой
    в объекте окна window (библиотека curses)
    на позиции x, y (y - строка терминала, x - столбец терминала).

    Если не указан параметр window, тогда вывод будет происходить в stderr.
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
    if window is None:
        for cur_char in itertools.cycle(spinner):
            print(cur_char, end='\r', file=sys.stderr, flush=True)
            await asyncio.sleep(0.1)
    else:
        for cur_char in itertools.cycle(spinner):
            window.refresh()
            window.addstr(y, x, cur_char)
            window.refresh()
            await asyncio.sleep(0.1)


async def print_paged(
    window: curses.window,
    loader: AsyncIterator[List[str]],
    header: List[str] = [],
    footer: List[str] = [],
    sep: List[str] = []
) -> None:
    """Разбивает список элементов на страницы и выводит их постранично.

    Параметры
    ---------
    window: curses.window
        Объект класса window модуля curses - окно,
        в котором будут отрисовываться страницы
    loader: AsyncIterator[List[str]]
        Асинхронный генератор элементов. В генераторе каждый элемент
        должен быть представлен в виде списка строк для вывода.
        Например, каждый элемент меню пиццерии может быть представлен
        в виде списка ["название пиццы", "описание пиццы"].
    header: List[str]
        Фиксированные строки, которые выводятся в верху экрана
    footer: List[str]
        Фиксированные строки, которые выводятся снизу экрана
    sep: List[str]
        Строки, которые используются как разделитель между элементами
    """

    # Получаем размеры окна
    MAX_ROWS = window.getmaxyx()[0]
    FREE_ROWS = MAX_ROWS - len(header) - len(footer) - 1

    def extend_pages(
        new_elements: List[List[str]],
        pages: List[List[str]]
    ) -> List[List[str]]:
        """Добавляет к текущим страницам новые элементы."""
        buffer = pages.pop()
        buffer_elements_count = buffer.pop()
        for element in new_elements:
            if not element:
                continue
            if len(buffer) >= FREE_ROWS:
                buffer.append(buffer_elements_count)
                pages.append(buffer)
                buffer = []
                buffer_elements_count = 0

            buffer_elements_count += 1
            buffer.extend(element)
            buffer.extend(sep)

        buffer.append(buffer_elements_count)
        pages.append(buffer)

        return pages

    async def load(loader):
        try:
            return await loader.__anext__()
        except StopAsyncIteration:
            return []
        # Произошла неизвестная ошибка
        except Exception:
            raise

    def print_all(page):
        window.clear()
        i = 0
        for s in header:
            if i >= curses.LINES:
                break
            window.addstr(i, 0, s)
            i += 1
        for s in page[offset:]:
            if i >= len(header) + FREE_ROWS:
                break
            if isinstance(s, int):
                break
            window.addstr(i, 0, s)
            i += 1
        for s in footer:
            if i >= curses.LINES:
                break
            window.addstr(i, 0, s)
            i += 1
        window.addstr(MAX_ROWS - 1, 0, PAGED_HELP)
        window.refresh()

    try:
        # Подгружаем первую пачку элементов,
        # формируем страницы и отображаем первую страницу
        window.clear()
        window.refresh()

        task_spinner = asyncio.create_task(
            load_spinner(window, len(header), 0))
        task_load = asyncio.create_task(load(loader))

        new_elements = await (task_load)
        task_spinner.cancel()

        pages = extend_pages(new_elements, [[0]])
        cur = 0  # номер текущей страницы
        offset = 0  # смещение по вертикали текущей страницы

        # Отображаем первую страницу
        print_all(pages[cur])

        # Слушаем клавиши
        while True:
            key = window.getch()

            if key == ord('q'):
                break
            if key == ord('a'):
                prev = cur
                cur = max(0, cur - 1)
                if prev != cur:
                    offset = 0
            if key == ord('d'):
                if cur + 1 >= len(pages) - 1:
                    window.clear()
                    window.refresh()
                    task_spinner = asyncio.create_task(
                        load_spinner(window, len(header), 0))
                    task_load = asyncio.create_task(load(loader))

                    new_elements = await (task_load)
                    task_spinner.cancel()

                    pages = extend_pages(new_elements, pages)
                prev = cur
                cur = min(cur + 1, len(pages) - 1)
                if prev != cur:
                    offset = 0

            if key == ord('s'):
                offset = min(
                    offset + 1,
                    FREE_ROWS - 1
                )
            if key == ord('w'):  # стрелка вверх
                offset = max(offset - 1, 0)

            # Отображаем новую страницу
            print_all(pages[cur])

    except Exception:
        curses.endwin()
        raise
    finally:
        curses.endwin()


def print_choices(
    window: curses.window,
    choices: List[str],
    header: List[str] = [],
    footer: List[str] = [],
    sep: List[str] = []
) -> int:
    """Разбивает список элементов на страницы и выводит их постранично.

    Параметры
    ---------
    window: curses.window
        Объект класса window модуля curses - окно,
        в котором всё будет отображаться
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
        Индекс выбранного элемента
        (0-индексация, относитеьлно списка choices)
    """

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
            for choice_index, choice in \
                    enumerate(choices[offset:offset + FREE_ROWS]):

                choice_index += offset
                if choice_index == selected_choice:
                    window.addstr(i, 0, choice, curses.A_BOLD)
                else:
                    window.addstr(i, 0, choice)
                i += 1
            for s in footer:
                window.addstr(i, 0, s)
                i += 1
            window.addstr(MAX_ROWS - 1, 0, CHOICES_HELP)
            window.refresh()

        print_choices()

        # Обрабатываем нажатия клавиш
        while True:
            key = window.getch()

            if key == ord('s'):
                selected_choice = min(
                    selected_choice + 1,
                    len(choices) - 1
                )
                if selected_choice >= offset + FREE_ROWS:
                    offset += 1
            if key == ord('w'):  # стрелка вверх
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
