from .repository import Repository
from .models import Pizza


class PizzaRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Pizza)

    def create(self, name: str, price: float, description: str = ''):
        return Pizza(name=name, description=description, price=price)

    def get_page(self, offset: int, limit: int) -> tuple:
        return self.session.query(Pizza).offset(offset).limit(limit).all()
