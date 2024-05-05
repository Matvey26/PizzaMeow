from .base import Base
from ..api import Session


class ShowCart(Base):
    def run(self, session : Session):
        show_id = self.options.show_id
        answer = session.get_cart_items()
        if isinstance(answer, str):
            print(f'{answer} Попробуйте снова')
            return
        for item in answer:
            if show_id:
                print(f"item id - {item['id']}")
            print(f"name pizza - {item['pizza_name']}")
            print(f"price - {item['price']}")
            print(f"quantity - {item['quantity']}")
            print(f"size - {item['size']}")
            print(f"dough - {item['dough']}\n")