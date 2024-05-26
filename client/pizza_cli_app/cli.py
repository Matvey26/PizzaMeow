"""Тут надо написать help"""

import argparse
import asyncio
from .commands import Base
from .commands import Config, ChangeEmail, ChangePasssword, ResetPasssword
from .commands import Logout, SignIn, SignUp, GetConfirmEmail
from .commands import Menu, Cart, Add, Change, Remove, Orders, Ingredients
from .commands import Checkout, Repeat, Cancel
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
        'orders': Orders,
        'repeat': Repeat,
        'cancel': Cancel,
        'get_confirm_email': GetConfirmEmail,
        'ingredients': Ingredients
    }

    session = Session()

    # Создаём экземпляр команды
    command = command_class.get(args.command, Base)(args, session)
    try:
        await command.run()
    finally:
        await session.close()


def main():
    """Точка входа в CLI"""
    parser = argparse.ArgumentParser()  # Главный парсер

    sub_parsers = parser.add_subparsers(dest='command')  # Парсер подкоманд

    # Регистрация
    sign_up = sub_parsers.add_parser('signup', help=SignUp.__doc__)
    sign_up.add_argument(
        'email',
        type=str,
        help="Почта, которая будет привязана к учётной записи."
    )

    # Вход
    sign_in = sub_parsers.add_parser('signin', help=SignIn.__doc__)
    sign_in.add_argument(
        'email',
        type=str,
        help="Почта, привязанная к учётной записи."
    )

    # Подкоманда reset_password
    reset_password = sub_parsers.add_parser(
        'reset_password', help=ResetPasssword.__doc__)
    reset_password.add_argument(
        'email',
        type=str,
        help="Почта, к которой привязана учётная запись."
    )

    # Смена пароля
    change_password = sub_parsers.add_parser(
        'change_password',
        help=ChangePasssword.__doc__
    )
    change_password.add_argument(
        'email',
        type=str,
        help="Почта, которая привязана к аккаунту."
    )

    # Ввести данные о пользователе
    config = sub_parsers.add_parser('config', help=Config.__doc__)
    config.add_argument(
        '--firstname',
        default=None,
        help='Имя пользователя.',
        type=str
    )
    config.add_argument(
        '--lastname',
        default=None,
        help='Фамилия пользователя.',
        type=str
    )
    config.add_argument(
        '--address',
        default=None,
        help='Адрес пользователя.',
        type=str
    )
    config.add_argument(
        '--phone',
        default=None,
        help='Номер телефона пользователя.',
        type=str
    )

    # Привязка новой почты к аккаунту
    change_email = sub_parsers.add_parser(
        'change_email',
        help=ChangeEmail.__doc__
    )
    change_email.add_argument(
        'old_email',
        type=str,
        help='Старая почта, к которой привязана учётная запись.'
    )
    change_email.add_argument(
        'new_email',
        type=str,
        help='Новая почта, которую требуется привязать к учётной записи.'
    )

    # Парсер выхода из приложения
    sub_parsers.add_parser('logout', help=Logout.__doc__)

    # Парсер для вывода меню
    menu = sub_parsers.add_parser('menu', help=Menu.__doc__)
    menu_arg_group = menu.add_mutually_exclusive_group()
    menu_arg_group.add_argument(
        '--show-id',
        action='store_true',
        dest='show_id',
        help='Показывать айди пицц.'
    )
    menu_arg_group.add_argument(
        '--no-show-id',
        action='store_false',
        dest='show_id',
        help='Не показывать айди пицц.'
    )
    # значение по умолчанию, если ни один из флагов не указан
    menu.set_defaults(show_id=True)
    menu.add_argument(
        '--with-preferences',
        '-p',
        action='store_false',
        default=True,
        dest='with_preferences',
        help='Отсортировать пиццы по предпочтительности'
    )

    # Парсер для вывода ингредиентов
    ingredients = sub_parsers.add_parser(
        'ingredients',
        help=Ingredients.__doc__
    )
    ingredients_arg_group = ingredients.add_mutually_exclusive_group()
    ingredients_arg_group.add_argument(
        '--show-id',
        action='store_true',
        dest='show_id',
        help='Показывать айди ингредиентов.'
    )
    ingredients_arg_group.add_argument(
        '--no-show-id',
        action='store_false',
        dest='show_id',
        help='Не показывать айди ингредиентов.'
    )
    # значение по умолчанию, если ни один из флагов не указан
    ingredients.set_defaults(show_id=True)

    # Парсер для показа содержимого корзины
    cart = sub_parsers.add_parser('cart', help=Cart.__doc__)
    cart_arg_group = cart.add_mutually_exclusive_group()
    cart_arg_group.add_argument(
        '--show-id',
        action='store_true',
        dest='show_id',
        help='Показывать айди элементов корзины.'
    )
    cart_arg_group.add_argument(
        '--no-show-id',
        action='store_false',
        dest='show_id',
        help='Не показывать айди элементов корзины.'
    )
    cart.set_defaults(show_id=True)

    # Парсер для добавления элемента в корзину
    add = sub_parsers.add_parser('add', help=Add.__doc__)
    add.add_argument(
        'pizza_id',
        type=int,
        help='ID пиццы, которая будет добавлена в корзину.'
    )
    add.add_argument(
        '--size',
        '-s',
        default=1,
        help='Размер пиццы.',
        type=int
    )
    add.add_argument(
        '--dough',
        '-d',
        default=1,
        help='Тесто для пиццы.',
        type=int
    )
    add.add_argument(
        '--quantity',
        '-q',
        default=1,
        help='Количество пицц.',
        type=int
    )
    add.add_argument(
        '--ingredients',
        '-i',
        default='',
        help='Ингредиенты пиццы.',
        type=str
    )

    # Парсер для изменения элемента корзины
    change = sub_parsers.add_parser('change', help=Change.__doc__)
    change.add_argument(
        'item_id',
        type=int,
        help='ID элемента корзины, который будет изменён.'
    )
    change.add_argument(
        'pizza_id',
        type=int,
        help='ID пиццы.'
    )
    change.add_argument(
        '--size',
        '-s',
        default=1,
        type=int,
        help='Размер пиццы.'
    )
    change.add_argument(
        '--dough',
        '-d',
        default=1,
        type=int,
        help='Размер пиццы.'
    )
    change.add_argument(
        '--quantity',
        '-q',
        default=1,
        type=int,
        help='Размер пиццы.'
    )

    change.add_argument(
        '--ingredients',
        '-i',
        default='',
        type=str,
        help='Ингредиенты.'
    )

    # Парсер для удаления элемента корзины
    remove = sub_parsers.add_parser('remove', help=Remove.__doc__)
    remove.add_argument(
        'item_id',
        type=int,
        help='ID элемента корзины, нужно удалить.'
    )

    # Парсер для создания заказа
    sub_parsers.add_parser('checkout', help=Checkout.__doc__)

    # Парсер для повторение заказа
    repeat = sub_parsers.add_parser('repeat', help=Repeat.__doc__)
    repeat.add_argument(
        'order_id',
        type=int,
        help='ID заказ, который надо повторить'
    )

    # Парсер для вывода истории заказов
    orders = sub_parsers.add_parser('orders', help=Orders.__doc__)
    orders_arg_group_id = orders.add_mutually_exclusive_group()
    orders_arg_group_id.add_argument(
        '--show-id',
        action='store_true',
        dest='show_id',
        help='Показывать айди заказов.'
    )
    orders_arg_group_id.add_argument(
        '--no-show-id',
        action='store_false',
        dest='show_id',
        help='Не показывать айди заказов.'
    )
    orders_arg_group_status = orders.add_mutually_exclusive_group()
    orders_arg_group_status.add_argument(
        '--active',
        '-a',
        help='Показать активные заказы.'
    )
    orders_arg_group_status.add_argument(
        '--completed',
        '-c',
        help='Показать незавершенные заказы.'
    )
    orders_arg_group_status.add_argument(
        '--all',
        '-A',
        help='Показать все заказы.'
    )
    orders.set_defaults(show_id=False)
    orders.set_defaults(active=True)
    orders.set_defaults(completed=False)
    orders.set_defaults(all=False)
    orders.set_defaults(no_show_id=True)

    # Отменить заказ
    cancel = sub_parsers.add_parser('cancel', help=Cancel.__doc__)
    cancel.add_argument(
        'order_id',
        type=int,
        help='ID заказа, который нужно отменить.'
    )

    # Получить письмо для подтверждения почты
    get_confirm_email = sub_parsers.add_parser(
        'get_confirm_email',
        help=GetConfirmEmail.__doc__
    )
    get_confirm_email.add_argument(
        'email',
        type=str,
        help='Почта, на которую нужно отправить письмо.'
    )

    args = parser.parse_args()
    asyncio.run(run_commands(args))
