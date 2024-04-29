from .base import Base
from ..api import Session

class RemoveItem(Base):
    def run(self, session : Session):
        item_id = self.options.item_id
        session.