from .base import Base
from ..api import Session


class Add(Base):
    """Добавляет новый объект в корзину"""
    def run(self, session : Session):
        pizza_id = self.options.pizza_id
        size = self.options.size
        dough = self.options.dough
        quantity = self.options.quantity
        data = {'pizza_id' : pizza_id, 'size' : size, 'dough' : dough, 'quantity' : quantity}
        response = session.add_item_to_cart(data)
        if response:
            print(response[1])
            return
        print('Пицца добавлена в корзину')