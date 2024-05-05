from ..api.api import Session
from .base import Base


class Menu(Base):
    """Команда для вывода меню пиццы"""

    def run(self, session: Session):
        show_id = self.options.show_id

        def get_all_pizzas():
            offset = 0
            limit = 20
            while (pizzas := session.get_pizzas_page(offset, limit)):
                data = []
                for pizza in pizzas:
                    rows = [
                        f"{pizza['id']}. {pizza['name']}.",
                        f"description: {pizza.get('description', '')}",
                        f"price: {pizza['price']}"
                    ]
                    data.append(rows)
                yield data
                offset += limit
            
        self.print_paged(get_all_pizzas())