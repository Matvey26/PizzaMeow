from . import pizza_repository
from flask import abort
from datetime import datetime, timedelta


def get_pizzas_page(offset: int, limit: int):
    page = pizza_repository.get_page(offset, limit)
    return pizza_repository.serialize(*page)


def get_pizza_by_id(pizza_id: int):
    pizza = pizza_repository.get(pizza_id)
    if pizza is None:
        abort(400, 'Пиццы с таким id нет.')
    return pizza_repository.serialize(pizza)[0]


def get_pizzas_preferences_page(
    offset: int,
    limit: int,
    user: str,
    token_info: dict
):
    user_id = int(user)
    page = pizza_repository.get_preferences_page(user_id, limit, offset)
    return pizza_repository.serialize(*page)

