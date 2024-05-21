import asyncio

from .base import Base
from ..utils.print_format import load_spinner


class Cancel(Base):
    """Отменить заказ"""

    async def run(self):
        order_id = self.options.order_id

        task_load = asyncio.create_task(load_spinner())
        task_cancel_order = asyncio.create_task(
            self.session.cancel_order(order_id)
        )

        response = await task_cancel_order
        task_load.cancel()

        if isinstance(response, tuple):
            print(response[1])
            return

        print('Заказ успешно отменён')
