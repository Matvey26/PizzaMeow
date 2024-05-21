from . import pizza_repository
from flask import abort


def get_pizzas_page(offset: int, limit: int):
    page = pizza_repository.get_page(offset, limit)
    return pizza_repository.serialize(*page)


def get_pizza_by_id(id: int):
    pizza = pizza_repository.get(id)
    if pizza is None:
        abort(400, 'Пиццы с таким id нет.')
    return pizza_repository.serialize(pizza)[0]
