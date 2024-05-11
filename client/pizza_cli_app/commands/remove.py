import asyncio
from .base import Base


class Remove(Base):
    """Удаляет элемент из корзины"""

    async def run(self):
        item_id = self.options.item_id

        task_load = asyncio.create_task(self.load_spinner())
        task_delete_item = asyncio.create_task(self.session.delete_item(item_id))

        response = await task_delete_item
        task_load.cancel()

        if response:
            print(response[1])
            return
        print('Элемент корзины успешно удалён из неё')
