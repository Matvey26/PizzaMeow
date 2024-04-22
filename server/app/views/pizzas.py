from . import pizza_repository
from . import user_repository
from flask import abort


def get_pizzas_page(offset: int, limit: int):
    page = pizza_repository.get_page(offset, limit)
    ret = []
    for pizza in page:
        ret.append(pizza_repository.serialize(pizza))
    return ret


def get_pizza_by_id(id: int):
    pizza = pizza_repository.get(id)
    if pizza is None:
        abort(400, 'Пиццы с таким id нет.')
    return pizza_repository.serialize(pizza)


def create_pizza(user, token_info, body):
    user_id = int(user)
    user = user_repository.get(user_id)
    if user.email != 'admin':
        abort(401, 'Вы не имеете достаточно прав, чтобы изменять этот ресурс.')
    
    name = body.get('name', '')
    price = body.get('price', 0)
    description = body.get('description', '')
    if name == '':
        abort(400, 'Нельзя создавать пиццу с пустым названием.')
    if price <= 0:
        abort(400, 'Нельзя создавать пиццу с отрицательной ценой.')

    new_pizza = pizza_repository.create(name, price, description=description)
    pizza_repository.save(new_pizza)

def update_pizza(user, token_info, id, body):
    user_id = int(user)
    user = user_repository.get(user_id)
    if user.email != 'admin':
        abort(401, 'Вы не имеете достаточно прав, чтобы изменять этот ресурс.')

    pizza = pizza_repository.get(int(id))
    if 'name' in body:
        name = body.get('name', '')
        if name == '':
            abort(400, 'Нельзя изменять название пицца на пустую строку.')
        pizza.name = name
    if 'price' in body:
        price = body.get('price', 0)
        if price <= 0:
            abort(400, 'Нельзя создавать пиццу с отрицательной ценой.')
        pizza.price = price
    if 'description' in body:
        description = body.get('description', '')
        pizza.description = description    

    pizza_repository.save(pizza)