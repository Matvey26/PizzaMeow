from .base import Base
from ..api import Session


class ShowCart(Base):
    def run(self, session : Session):
        show_id = self.options.show_id
        answer = session.get_cart_items()

        if isinstance(answer, tuple):
            print(answer[1])
            return
        
        print('Корзина:')
        print(f"Цена корзины: {answer['total_price']}")
        for item in answer['cart_items']:
            print('--------------------------------')
            if show_id:
                print(f"item id: {item['id']}")
            print(f"Цена - {item['total_price']}")
            print(f"Название пиццы - {item['pizza_name']}")
            print(f"Количество - {item['quantity']}")
            print(f"Размер пиццы - {item['size']}")
            print(f"Тип теста - {item['dough']}\n")
        print('--------------------------------')