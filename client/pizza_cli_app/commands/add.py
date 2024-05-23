import asyncio

from .base import Base
from ..utils.print_format import load_spinner


class Add(Base):
    """Добавляет новый объект в корзину"""

    async def run(self):
        pizza_id = self.options.pizza_id
        size = self.options.size
        dough = self.options.dough
        quantity = self.options.quantity
        ingredients = []
        if self.options.ingredients != -1:
            for ingredient in self.options.ingredients.split(', '):
                    ing_id, count_ing = ingredient.split(':')
                    ingredients.append({ing_id : count_ing})
                    if int(count_ing) < 0:
                        print('Введено отрицательное количество ингредиента')
                        return 
        data = {
            'pizza_id': pizza_id,
            'size': size,
            'dough': dough,
            'quantity': quantity,
            'ingredients' : ingredients
        }

        task_load = asyncio.create_task(load_spinner())
        task_add_item_to_cart = asyncio.create_task(
            self.session.add_item_to_cart(data)
        )

        response = await task_add_item_to_cart
        task_load.cancel()

        if response:
            print(response[1])
            return
        print('Пицца добавлена в корзину')
