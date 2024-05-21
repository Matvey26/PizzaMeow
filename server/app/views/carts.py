from . import user_repository
from . import pizza_repository
from . import cart_repository
from . import cart_item_repository
from flask import abort
from ..model.models import PizzaSizeEnum, PizzaDoughEnum


conv_size_enum = {
    0: 'small',
    1: 'medium',
    2: 'large',
    'small': 'small',
    'medium': 'medium',
    'large': 'large'
}

conv_dough_enum = {
    0: 'thin',
    1: 'classic',
    'thin': 'thin',
    'classic': 'classic'
}


def get_cart(user, token_info):
    user_id = int(user)
    user = user_repository.get(user_id)
    cart = cart_repository.get_by_user(user)
    return cart_repository.serialize(cart)


def add_item_to_cart(user, token_info, body):
    user_id = int(user)
    user = user_repository.get(user_id)
    cart = cart_repository.get_by_user(user)

    if 'pizza_id' not in body:
        abort(400, 'Обязательно нужно указать pizza_id.')
    pizza = pizza_repository.get(body['pizza_id'])
    if pizza is None:
        abort(400, 'Такой пиццы не существует =(')
    quantity = body.get('quantity', 1)
    try:
        size = conv_size_enum[body.get('size', 1)]
        dough = conv_dough_enum[body.get('dough', 1)]
    except:
        abort(400, 'Неверный формат поля size или dough.')
    total_price = pizza.price * quantity

    cart_item = cart_item_repository.create(
        pizza=pizza,
        total_price=total_price,
        quantity=quantity,
        size=size,
        dough=dough
    )

    cart_repository.add_item(cart, cart_item)


def update_item_in_cart(user, token_info, item_id, body):
    user_id = int(user)
    user = user_repository.get(user_id)
    cart = cart_repository.get_by_user(user)

    cart_item = cart_item_repository.get(item_id)
    if cart_item.cart_id != cart.id:
        abort(400, 'В вашей корзине нет такого объекта.')

    if 'pizza_id' in body:
        pizza = pizza_repository.get(body['pizza_id'])
        if pizza is None:
            abort(400, 'Такой пиццы не существует =(')
        cart_item.pizza = pizza
    if 'quantity' in body:
        cart_item.quantity = body['quantity']
    try:
        if 'size' in body:
            cart_item.size = conv_size_enum[body['size']]
        if 'dough' in body:
            cart_item.dough = conv_dough_enum[body['dough']]
    except:
        abort(400, 'Неверный формат полей size или dough.')
    cart_item.total_price = cart_item.quantity * cart_item.pizza.price

    cart_item_repository.update(cart_item)


def remove_item_from_cart(user, token_info, item_id):
    user_id = int(user)
    user = user_repository.get(user_id)
    cart = cart_repository.get_by_user(user)
    cart_item = cart_item_repository.get(item_id)
    if cart_item is None or cart_item.cart_id != cart.id:
        abort(400, 'В вашей корзине нет такого объекта.')

    cart_item_repository.delete(cart_item)
