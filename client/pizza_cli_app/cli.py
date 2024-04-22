"""Тут надо написать help"""

import argparse
import sys
from .commands import Base, ChangeEmail, ChangePasssword, Config, Logout, Menu, ResetPasssword, SignIn, SignUp
from .api import Session

def main():
    """Точка входа в CLI"""
    parser = argparse.ArgumentParser()  # Главный парсер

    sub_parsers = parser.add_subparsers(dest='command')  # Парсер подкоманд

    # Регистрация
    sign_up = sub_parsers.add_parser('signup', help=SignUp.__doc__)
    sign_up.add_argument('email', type=str, help="Почта, которая будет привязана к учётной записи.")

    # Вход
    sign_in = sub_parsers.add_parser('signin', help=SignIn.__doc__)
    sign_in.add_argument('email', type=str, help="Почта, привязанная к учётной записи.")

    # Подкоманда reset_password
    reset_password = sub_parsers.add_parser('reset_password', help=ResetPasssword.__doc__)
    reset_password.add_argument('email', type=str, help="Почта, к которой привязана учётная запись.")

    # Смена пароля
    change_password = sub_parsers.add_parser('changepassword', help=ChangePasssword.__doc__)
    change_password.add_argument('--email', type=str, help="Почта, которая привязана к аккаунту.")

    # Ввести данные о пользователе
    config = sub_parsers.add_parser('config', help=Config.__doc__)
    config.add_argument('--firstname', default=None, help='Имя пользователя.', type=str)
    config.add_argument('--lastname', default=None, help='Фамилия пользователя.', type=str)
    config.add_argument('--address', default=None, help='Адрес пользователя.', type=str)
    config.add_argument('--phone', default=None, help='Номер телефона пользователя.', type=str)
    
    # Привязка новой почты к аккаунту
    change_email = sub_parsers.add_parser('change_email', help=ChangeEmail.__doc__)
    change_email.add_argument('old_email', type=str, help='Старая почта, к которой привязана учётная запись.')
    change_email.add_argument('new_email', type=str, help='Новая почта, которую требуется привязать к учётной записи.')

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
        'menu': Menu,
        'reset_password': ResetPasssword,
        'change_email': ChangeEmail,
        'change_password': ChangePasssword
    }

    session = Session()
    
    command = command_class.get(args.command, Base)(args)  # Создаём экземпляр команды
    command.run(session)
