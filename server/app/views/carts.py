from . import user_repository
from . import pizza_repository
from . import cart_repository
from . import cart_item_repository
from . import ingredient_repository
from . import cart_item_ingredient_repository
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
    for ser_ingredient in ingredients:
        if 'quantity' not in ser_ingredient or \
                'id' not in ser_ingredient:
            abort(400, 'Неверный формат списка выбранных ингредиентов.')
        ingredient = ingredient_repository.get(ser_ingredient['id'])
        if ingredient is None:
            abort(400, 'Такого ингредиента не существует.')
        all_ingredients_quantity += ser_ingredient['quantity']
        ingredients_total_price += ingredient.price * \
            ser_ingredient['quantity']

    if all_ingredients_quantity > 15:
        abort(
            400, f'Вы выбрали слишком много ингридиентов, {all_ingredients_quantity} > 15.')

    # Считаем итоговую цену
    total_price = pizza.price * quantity + ingredients_total_price

    cart_item = cart_item_repository.create(
        pizza=pizza,
        total_price=total_price,
        quantity=quantity,
        size=size,
        dough=dough,
        ingredients=ingredients
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

    ingredients_total_price = 0
    if 'ingredients' in body:
        try:
            new_ingredients_map = {}
            for item in body['ingredients']:
                new_ingredients_map[item['id']] = item['quantity']
                if ingredient_repository.get(item['id']) is None:
                    abort(400, 'Не существует такого ингредиента')
        except KeyError:
            abort(400, 'Неверный формат ингредиентов.')

        for cart_item_ingredient in cart_item.ingredients:
            if cart_item_ingredient.id in new_ingredients_map:
                cart_item_ingredient.quantity = \
                    new_ingredients_map[cart_item_ingredient.id]
                del new_ingredients_map[cart_item_ingredient.id]

        for ing_id, ing_cnt in new_ingredients_map.items():
            cart_item.ingredients.append(
                cart_item_ingredient_repository.create(
                    ingredient_id=ing_id,
                    quantity=ing_cnt
                )
            )

    cart_item.total_price = cart_item.quantity * \
        cart_item.pizza.price + ingredients_total_price

    cart_item_repository.update(cart_item)


def remove_item_from_cart(user, token_info, item_id):
    user_id = int(user)
    user = user_repository.get(user_id)
    cart = cart_repository.get_by_user(user)
    cart_item = cart_item_repository.get(item_id)
    if cart_item is None or cart_item.cart_id != cart.id:
        abort(400, 'В вашей корзине нет такого объекта.')

    cart_item_repository.delete(cart_item)
