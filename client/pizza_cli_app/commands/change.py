import asyncio
from .base import Base


class Change(Base):
    """Изменяет сущесвтующий элемент корзины"""

    async def run(self):
        item_id = self.options.item_id
        pizza_id = self.options.pizza_id
        size = self.options.size
        dough = self.options.dough
        quantity = self.options.quantity
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

        task_load = asyncio.create_task(
            self.load_spinner()
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
