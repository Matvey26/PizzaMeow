from ..api.api import Session
from .base import Base


class Menu(Base):
    """Команда для вывода меню пиццы"""

    def run(self, session: Session):
        show_id = self.options.show_id
        limit = self.options.limit

        def get_all_pizzas():
            offset = 0
            while (pizzas := session.get_pizzas_page(offset, limit)):
                if isinstance(pizzas, tuple):
                    raise Exception(pizzas[1])
                data = []
                for pizza in pizzas:
                    rows = [
                        f"{pizza['id']}. {pizza['name']}." if show_id else f"{pizza['name']}",
                        f"description: {pizza.get('description', '')}",
                        f"price: {pizza['price']}"
                    ]
                    data.append(rows)
                yield data
                offset += limit
        try:
            self.print_paged(limit, get_all_pizzas())
        except Exception as e:
            print(e)
            raise