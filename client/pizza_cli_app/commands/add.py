import asyncio

from .base import Base
from ..utils.print_format import load_spinner
from ..utils.similarity_search import search_by_similarity


class Add(Base):
    """Добавляет новый объект в корзину"""

    async def run(self):
        pizza_id = self.options.pizza_id
        if pizza_id.isdigit():
            pizza_id = int(pizza_id)
        else:
            task_load = asyncio.create_task(load_spinner())

            async def get_all_pizzas():
                offset = 0
                limit = 40
                while (
                    pizzas := await self.session.get_pizzas_page(
                        offset,
                        limit,
                        with_preferences=False
                    )
                ):
                    if isinstance(pizzas, tuple):
                        raise Exception(pizzas[1])
                    yield pizzas
                    offset += limit

            all_pizzas = []
            async for i in get_all_pizzas():
                all_pizzas.extend(i)

            similar_pizzas = search_by_similarity(
                all_pizzas,
                threshold=80,
                name=pizza_id
            )

            if len(similar_pizzas) == 1:
                pizza_id = similar_pizzas[0]['id']
            else:
                print('Введите более точное название')
                for pizza in similar_pizzas:
                    print(f'{pizza["id"]}. {pizza["name"]}')
                return

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
