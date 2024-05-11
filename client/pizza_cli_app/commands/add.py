import asyncio
from .base import Base


class Add(Base):
    """Добавляет новый объект в корзину"""

    async def run(self):
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

        task_load = asyncio.create_task(self.load_spinner())
        task_add_item_to_cart = asyncio.create_task(self.session.add_item_to_cart(data))

        response = await task_add_item_to_cart
        task_load.cancel()
        
        if response:
            print(response[1])
            return
        print('Пицца добавлена в корзину')
