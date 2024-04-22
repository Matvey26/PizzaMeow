"""Тут надо написать help"""

import argparse
import sys
from .commands import Base, Config, SignUp, SignIn, Logout, Menu, ResetPasssword
from .api import Session

def main():
    """Точка входа в CLI"""
    parser = argparse.ArgumentParser()  # Главный парсер

    sub_parsers = parser.add_subparsers(dest='command')  # Парсер подкоманд

    # Подкоманда sing_up, зарегистрироваться
    sign_up = sub_parsers.add_parser('signup', help=SignUp.__doc__)
    sign_up.add_argument('--email', type=str, help="Почта, которая будет привязана к аккаунту.")

    # Подкоманда sign_in
    sign_in = sub_parsers.add_parser('signin', help=SignIn.__doc__)
    sign_in.add_argument('--email', type=str, help="Почта, которая будет привязана к аккаунту.")

    # Подкоманда reset_password
    reset_password = sub_parsers.add_parser('resetpassword', help=SignIn.__doc__)
    reset_password.add_argument('--email', type=str, help="Почта, которая будет привязана к аккаунту.")

    # Ввести данные о пользователе
    config = sub_parsers.add_parser('config', help=Config.__doc__)
    config.add_argument('--firstname', default=None, help='Имя пользователя.', type=str)
    config.add_argument('--lastname', default=None, help='Фамилия пользователя.', type=str)
    config.add_argument('--address', default=None, help='Адрес пользователя.', type=str)
    config.add_argument('--phone', default=None, help='Номер телефона пользователя.', type=str)
    config.add_argument('--change-password', action='store_true')
    # config.add_argument('--reset-password', default='', help='На указанную почту отправляет новый пароль.')
    # config.add_argument('--change-email', nargs=2, metavar=("old_email", "new_email"), help='Меняет')

    # Парсер выхода из приложения
    logout = sub_parsers.add_parser('logout', help=Logout.__doc__)

    # Парсер для вывода меню
    menu = sub_parsers.add_parser('menu', help=Menu.__doc__)
    menu.add_argument('--show-id', action='store_true', help='Показывать айди пицц.')
    menu.add_argument('--no-show-id', action='store_false', help='Не показывать айди пицц.')
    menu.add_argument('--limit', default=20, help='Максимум пицц в странице.')

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
