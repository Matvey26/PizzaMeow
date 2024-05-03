from .base import Base
from ..api import Session

class ChangeCart(Base):
    def run(self, session : Session):
        item_id = self.options.item_id
        pizza_id = self.options.pizza_id
        size = self.options.size
        dough = self.options.dough
        quantity = self.options.quantity
        data = {'item_id' : item_id, 'pizza_id' : pizza_id, 'size' : size, 'dough' : dough, 'quantity' : quantity}
        response = session.update_item_in_cart(data)
        if response == '400':
            print(f'Успешно изменили {item_id}')
            return
        print(f'Изменение не успешно {item_id}')