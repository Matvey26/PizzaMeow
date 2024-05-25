"""Тут надо написать help"""

import argparse
from .commands import Base, Create, Delete


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
        help='ID записи, которую нужно удалить'
    )

    args = parser.parse_args()

    command_class = {
        'create': Create,
        'delete': Delete
    }

    command = command_class.get(args.command, Base)(
        args)  # Создаём экземпляр команды
    command.run()
