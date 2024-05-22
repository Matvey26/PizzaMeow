from . import user_repository
from . import pizza_repository
from . import cart_repository
from . import cart_item_repository
from . import ingredient_repository
from flask import abort


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
    if user is None:
        abort(400, 'Токен недействителен.')
    cart = cart_repository.get_by_user(user)
    return cart_repository.serialize(cart)


def add_item_to_cart(user, token_info, body):
    user_id = int(user)
    user = user_repository.get(user_id)
    cart = cart_repository.get_by_user(user)

    # Обрабатываем ID пиццы
    if 'pizza_id' not in body:
        abort(400, 'Обязательно нужно указать pizza_id.')
    pizza = pizza_repository.get(body['pizza_id'])
    if pizza is None:
        abort(400, 'Такой пиццы не существует =(')

    # Обрабатываем количество пицц
    quantity = body.get('quantity', 1)

    # Обрабатываем размер и тесто пиццы
    try:
        size = conv_size_enum[body.get('size', 1)]
        dough = conv_dough_enum[body.get('dough', 1)]
    except ValueError:
        abort(400, 'Неверный формат поля size или dough.')

    # Обрабатываем список выбранных ингридиентов
    ingredients = body.get('ingredients', [])
    all_ingredients_quantity = 0
    ingredients_total_price = 0
    for pair_ingredient in ingredients:
        if 'quantity' not in pair_ingredient or \
                'id' not in pair_ingredient:
            abort(400, 'Неверный формат списка выбранных ингредиентов.')
        if pair_ingredient['quantity'] < 0:
            abort(400, 'Количество ингридиентов не может быть отрицательным.')
        ingredient = ingredient_repository.get(pair_ingredient['id'])
        all_ingredients_quantity += pair_ingredient['quantity']
        ingredients_total_price += ingredient.price * pair_ingredient['quantity']

    if all_ingredients_quantity > 15:
        abort(400, f'Вы выбрали слишком много ингридиентов, {all_ingredients_quantity} > 15.')

    # Считаем итоговую цену
    total_price = pizza.price * quantity + ingredients_total_price

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
    except ValueError:
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
