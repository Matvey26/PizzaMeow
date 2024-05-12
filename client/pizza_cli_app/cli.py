"""Тут надо написать help"""

import argparse
import asyncio
from .commands import Base
from .commands import Config, ChangeEmail, ChangePasssword, ResetPasssword
from .commands import Logout, SignIn, SignUp
from .commands import Menu, Cart, Add, Change, Remove, Checkout, Orders
from .api import Session


async def run_commands(args):
    command_class = {
        'signup': SignUp,
        'signin': SignIn,
        'config': Config,
        'logout': Logout,
        'menu': Menu,
        'reset_password': ResetPasssword,
        'change_email': ChangeEmail,
        'change_password': ChangePasssword,
        'cart': Cart,
        'add': Add,
        'change': Change,
        'remove': Remove,
        'checkout': Checkout,
        'orders': Orders
    }

    session = Session()
    
    # Создаём экземпляр команды
    command = command_class.get(args.command, Base)(args, session)
    try:
        await command.run()
    except Exception:
        await session.close()
        raise

    await session.close()


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
    change_password = sub_parsers.add_parser('change_password', help=ChangePasssword.__doc__)
    change_password.add_argument('email', type=str, help="Почта, которая привязана к аккаунту.")

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
    menu_arg_group = menu.add_mutually_exclusive_group()
    menu_arg_group.add_argument('--show-id', action='store_true', dest='show_id', help='Показывать айди пицц.')
    menu_arg_group.add_argument('--no-show-id', action='store_false', dest='show_id', help='Не показывать айди пицц.')
    menu.set_defaults(show_id=True)  # значение по умолчанию, если ни один из флагов не указан
    menu.add_argument('--limit', default=20, type=int, help='Максимум пицц в странице.')

    # Парсер для показа содержимого корзины
    cart = sub_parsers.add_parser('cart', help=Cart.__doc__)
    cart_arg_group = cart.add_mutually_exclusive_group()
    cart_arg_group.add_argument('--show-id', action='store_true', dest='show_id', help='Показывать айди элементов корзины.')
    cart_arg_group.add_argument('--no-show-id', action='store_false', dest='show_id', help='Не показывать айди элементов корзины.')
    cart.set_defaults(show_id=True)
    cart.add_argument('--limit', default=20, type=int, help='Максимум элементов корзины на странице.')

    # Парсер для добавления элемента в корзину
    add = sub_parsers.add_parser('add', help=Add.__doc__)
    add.add_argument('pizza_id', type=int, help='ID пиццы, которая будет добавлена в корзину.')
    add.add_argument('--size', default=1, help='Размер пиццы.', type=int)
    add.add_argument('--dough', default=1, help='Размер пиццы.', type=int)
    add.add_argument('--quantity', default=1, help='Размер пиццы.', type=int)

    # Парсер для изменения элемента корзины
    change = sub_parsers.add_parser('change', help=Change.__doc__)
    change.add_argument('item_id', type=int, help='ID элемента корзины, который будет изменён.')
    change.add_argument('--pizza_id', default=-1, type=int, help='ID пиццы.')
    change.add_argument('--size', default=-1, type=int, help='Размер пиццы.')
    change.add_argument('--dough', default=-1, type=int, help='Размер пиццы.')
    change.add_argument('--quantity', default=-1, type=int, help='Размер пиццы.')

    # Парсер для удаления элемента корзины
    remove = sub_parsers.add_parser('remove', help=Remove.__doc__)
    remove.add_argument('item_id', type=int, help='ID элемента корзины, нужно удалить.')

    # Парсер для создания заказа
    checkout  = sub_parsers.add_parser('checkout', help=Checkout.__doc__)

    # Парсер для вывода истории заказов
    orders = sub_parsers.add_parser('orders', help=Orders.__doc__)
    orders.add_argument('--limit', default=20, type=int, help='Максимум заказов на странице')
    orders_arg_group_id = orders.add_mutually_exclusive_group()
    orders_arg_group_id.add_argument('--show-id', action='store_true', dest='show_id', help='Показывать айди заказов.')
    orders_arg_group_id.add_argument('--no-show-id', action='store_false', dest='show_id', help='Не показывать айди заказов.')
    orders_arg_group_status = orders.add_mutually_exclusive_group()
    orders_arg_group_status.add_argument('--active', help='Показать активные заказы.')
    orders_arg_group_status.add_argument('--completed', help='Показать незавершенные заказы.')
    orders_arg_group_status.add_argument('--all', help='Показать все заказы.')
    orders.set_defaults(show_id=False)
    orders.set_defaults(active=True)
    orders.set_defaults(completed=False)
    orders.set_defaults(all=False)
    orders.set_defaults(no_show_id=True)

    args = parser.parse_args()
    asyncio.run(run_commands(args))