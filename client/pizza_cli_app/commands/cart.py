from .base import Base
from ..api import Session


class ShowCart(Base):
    def run(self, session : Session):
        show_id = self.options.show_id
        answer = session.get_cart_items()

        if isinstance(answer, tuple):
            print(answer[1])
            return
        
        header = [
            f"Цена корзины: {answer['total_price']}",
            '+++++++++++++++++++++++++++++'
        ]
        sep = [
            '-----------------------------'
        ]
        elements = []
        for item in answer['cart_items']:
            element = []
            if show_id:
                element.append(f"ID элемента корзины: {item['id']}")
            element.append(f"Цена - {item['total_price']}")
            element.append(f"Название пиццы - {item['pizza_name']}")
            element.append(f"Количество - {item['quantity']}")
            element.append(f"Размер пиццы - {item['size']}")
            element.append(f"Тип теста - {item['dough']}\n")
            elements.append(element)
        self.print_paged(iter([elements]), header=header, sep=sep)