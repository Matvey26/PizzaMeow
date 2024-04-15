"""Тут надо написать help"""

import argparse
import sys
from .commands import Base, SignUp, SignIn, Config, Logout, Menu
from .api import Session

def main():
    """Точка входа в CLI"""
    parser = argparse.ArgumentParser()  # Главный парсер

    sub_parsers = parser.add_subparsers(dest='command')  # Парсер подкоманд

    # Подкоманда sing_up, зарегистрироваться
    registration_parser = sub_parsers.add_parser('signup', help=SignUp.__doc__)
    registration_parser.add_argument('--email', type=str, help="Введите почту")

    # Подкоманда sign_in
    sign_in = sub_parsers.add_parser('signin', help=SignIn.__doc__)
    sign_in.add_argument('--email', type=str, help="Введите почту")

    # Ввести данные о пользователе
    config = sub_parsers.add_parser('config', help=Config.__doc__)
    config.add_argument("--firstname", help="the first name of the customer", type=str)
    config.add_argument("--lastname", help="the last name of the customer", type=str)
    config.add_argument("--address", help="the address of the customer", type=str)
    config.add_argument("--phone", help="the phone number of the customer", type=str)

    # Парсер выхода из приложения
    logout = sub_parsers.add_parser('logout', help=Logout.__doc__)

    args = parser.parse_args()

    command_class = {
        'signup' : SignUp,
        'signin' : SignIn,
        'config' : Config,
        'logout' : Logout,
        'menu': Menu
    }

    session = Session()
    
    command = command_class.get(args.command, Base)(args)  # Создаём экземпляр команды
    command.run(session)
