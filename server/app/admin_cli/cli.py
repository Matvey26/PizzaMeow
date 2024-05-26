"""Тут надо написать help"""

import argparse
from .commands import Base, Create, Delete, Find


def main():
    """Точка входа в CLI"""
    parser = argparse.ArgumentParser()  # Главный парсер

    sub_parsers = parser.add_subparsers(dest='command')  # Парсер подкоманд

    create = sub_parsers.add_parser('create', help=Create.__doc__)
    create.add_argument(
        'tablename',
        type=str,
        help='Название таблицы'
    )
    create.add_argument(
        '-k',
        '--key',
        action='append',
        nargs=2,
        metavar=('KEY', 'VALUE'),
        help='Именованные аргументы для конструктора'
    )

    delete = sub_parsers.add_parser('delete', help=Delete.__doc__)
    delete.add_argument(
        'tablename',
        type=str,
        help='Название таблицы'
    )
    delete.add_argument(
        'id',
        type=int,
        help='ID записи, которую нужно удалить. '
        'Введите -1, если хотите удалить всё.'
    )

    find = sub_parsers.add_parser('find', help=Find.__doc__)
    find.add_argument(
        'tablename',
        type=str,
        help='Название таблицы'
    )
    find.add_argument(
        '-k',
        '--key',
        action='append',
        nargs=2,
        metavar=('KEY', 'VALUE'),
        help='Пары вида: <название поля, значение поля>'
    )

    args = parser.parse_args()

    command_class = {
        'create': Create,
        'delete': Delete,
        'find': Find
    }

    # Создаём экземпляр команды
    command = command_class.get(args.command, Base)(
        args
    )
    command.run()
