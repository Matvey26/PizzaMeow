"""Тут надо написать help"""

import argparse
import sys
from .commands import Base, Registration, Entrance, Config

def main():
    """Точка входа в CLI"""
    parser = argparse.ArgumentParser()  # Главный парсер

    # Вывод собственного сообщения справки
    if "-h" in sys.argv or "--help" in sys.argv:
        # print(custom_help)
        parser.print_help()

    sub_parsers = parser.add_subparsers(dest='command')  # Парсер подкоманд
    
    # Подкоманда registration
    registration_parser = sub_parsers.add_parser('sign_up', help=Registration.__doc__)
    registration_parser.add_argument('--email', type=str, help="Введите почту")

    # Подкоманда sign_in
    sign_in = sub_parsers.add_parser('sign_in', help=Entrance.__doc__)
    sign_in.add_argument('--email', type=str, help="Введите почту")
    
    # Ввести данные о пользователе
    pers_data = sub_parsers.add_parser('config', help=Config.__doc__)
    pers_data.add_argument("--firstname", help="the first name of the customer", type=str)
    pers_data.add_argument("--lastname", help="the last name of the customer", type=str)
    pers_data.add_argument("--address", help="the address of the customer", type=str)
    pers_data.add_argument("--phone", help="the phone number of the customer", type=str)

    args = parser.parse_args()

    command_class = {
        'sign_up' : Registration,
        'sign_in' : Entrance,
        'config' : Config,
    }


    command = command_class.get(args.command, Base)(args)  # Создаём экземпляр команды
    command.run()