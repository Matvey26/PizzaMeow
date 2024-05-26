import asyncio

from .base import Base
from ..utils.print_format import load_spinner


class Change(Base):
    """Изменяет существующий элемент корзины"""

    async def run(self):
        item_id = self.options.item_id
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

        if quantity == 0:
            self.session.delete_item(item_id)
            return

        data = {}
        if pizza_id > -1:
            data['pizza_id'] = pizza_id
        if size > -1:
            data['size'] = size
        if dough > -1:
            data['dough'] = dough
        if quantity > -1:
            data['quantity'] = quantity
        if ingredients is not None:
            data['ingredients'] = ingredients
        task_load = asyncio.create_task(
            load_spinner()
        )
        task_update_item_in_cart = asyncio.create_task(
            self.session.update_item_in_cart(item_id, data)
        )

        response = await task_update_item_in_cart
        task_load.cancel()

        if response:
            print(response[1])
            return
        print(f'Элемент корзины {item_id} успешно изменён')
