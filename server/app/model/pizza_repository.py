from .repository import Repository
from .models import Pizza

class PizzaRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Pizza)

    def create_pizza(self, name : str, description : str, price : float):
        new_pizza = Pizza(name=name, description=description, price=price)
        self.session.add(new_pizza)
        self.session.commit(new_pizza)

    def change_parametrs(self, pizza : Pizza, new_name=None, new_description=None, new_price=None):
        if new_name:
            pizza.name = new_name
        if new_description:
            pizza.description = new_description
        if new_price:
            pizza.price = new_price
        self.session.commit(pizza)

    def delete_pizza(self, pizza : Pizza):
        deleted = self.session.delete(pizza)
        self.session.commit()
        return deleted
