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
        if self.options.ingredients != '':
            for pair_ingredient in self.options.ingredients.split(','):
                pair_ingredient = pair_ingredient.strip()
                if ':' not in pair_ingredient:
                    print('Неверный формат ингредиентов.')
                    return
                ing_id, count_ing = pair_ingredient.split(':')
                ingredients.append({
                    'id': int(ing_id),
                    'quantity': int(count_ing)
                })
                if int(count_ing) < 0:
                    print('Введено отрицательное количество ингредиента')
                    return
        data = {
            'pizza_id': pizza_id,
            'size': size,
            'dough': dough,
            'quantity': quantity,
            'ingredients': ingredients
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
