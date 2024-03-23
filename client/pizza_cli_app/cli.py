"""Тут надо написать help"""

import argparse
from .commands import Base, HelloWorld

def main():
    """Точка входа в CLI"""
    parser = argparse.ArgumentParser(description='Some')  # Главный парсер
    sub_parsers = parser.add_subparsers(dest='command')  # Парсер подкоманд
    hello_parser = sub_parsers.add_parser('helloworld', help=HelloWorld.__doc__)  # Подкоманда helloworld

    args = parser.parse_args()

    command_class = {
        'helloworld': HelloWorld
    }

    command = command_class.get(args.command, Base)(args)  # Создаём экземпляр команды
    command.run()