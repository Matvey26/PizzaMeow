from .base import Base
from ..api import Session

class AddCart(Base):
    def run(self, session : Session):
        pizza_id = self.options.pizza_id
        size = self.options.size
        dough = self.options.dough
        quantity = self.options.quantity
        data = {'pizza_id' : pizza_id, 'size' : size, 'dough' : dough, 'quantity' : quantity}
        response = session.add_item_to_cart(data)
        if response == '400':
            print(f'Добавление прошло успешно!')
            return
        print(f'Добавление прошло не успешно.')