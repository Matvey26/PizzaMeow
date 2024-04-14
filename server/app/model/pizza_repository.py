from .repository import Repository
from .models import Pizza

class PizzaRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Pizza)

    def create(self, name: str, description: str, price: float):
        return Pizza(name=name, description=description, price=price)