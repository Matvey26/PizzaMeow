from .base import Base
from ..api import Session


class Change(Base):
    def run(self, session : Session):
        item_id = self.options.item_id
        pizza_id = self.options.pizza_id
        size = self.options.size
        dough = self.options.dough
        quantity = self.options.quantity
        data = {'pizza_id' : pizza_id, 'size' : size, 'dough' : dough, 'quantity' : quantity}
        response = session.update_item_in_cart(item_id, data)
        if response:
            print(response[1])
            return
        print(f'Элемент корзины {item_id} успешно изменён')
