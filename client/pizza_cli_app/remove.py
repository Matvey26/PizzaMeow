from .base import Base
from ..api import Session

class RemoveItem(Base):
    def run(self, session : Session):
        item_id = self.options.item_id
        response = session.delete_item(item_id)
        if response == '400':
            print(f'Успешно удалили {item_id}')
            return
        print(f'Не успешно удалили {item_id}')