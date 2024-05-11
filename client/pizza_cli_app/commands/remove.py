from .base import Base


class Remove(Base):
    """Удаляет элемент из корзины"""

    def run(self):
        item_id = self.options.item_id
        response = self.session.delete_item(item_id)
        if response:
            print(response[1])
            return
        print('Элемент корзины успешно удалён из неё')
