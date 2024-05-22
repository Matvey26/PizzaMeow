from .repository import Repository
from .models import Ingredient


class IngredientRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Ingredient)

    def create(self, name: str, price: float, description: str = ''):
        return Ingredient(name=name, price=price, description=description)
