from .base import Base
from ..api import Session


class Remove(Base):
    """Удаляет элемент из корзины"""
    def run(self, session : Session):
        item_id = self.options.item_id
        response = session.delete_item(item_id)
        if response:
            print(response[1])
            return
        print('Элемент корзины успешно удалён из неё')