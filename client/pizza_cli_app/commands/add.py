from .base import Base


class Add(Base):
    """Добавляет новый объект в корзину"""

    def run(self):
        pizza_id = self.options.pizza_id
        size = self.options.size
        dough = self.options.dough
        quantity = self.options.quantity
        data = {
            'pizza_id': pizza_id,
            'size': size,
            'dough': dough,
            'quantity': quantity
        }
        response = self.session.add_item_to_cart(data)
        if response:
            print(response[1])
            return
        print('Пицца добавлена в корзину')
