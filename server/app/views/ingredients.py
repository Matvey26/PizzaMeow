from . import ingredient_repository
from flask import abort


def get_ingredients_page(offset: int, limit: int):
    page = ingredient_repository.get_page(offset, limit)
    return ingredient_repository.serialize(*page)


def get_ingredient_by_id(ingredient_id: int):
    ingredient = ingredient_repository.get(ingredient_id)
    if ingredient is None:
        abort(400, 'Ингредиента с таким id нет.')
    return ingredient_repository.serialize(ingredient)[0]
