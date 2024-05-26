from .repository import Repository
from .models import Pizza, Order, OrderItem
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased


class PizzaRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Pizza)

    def create(self, name: str, price: float, description: str = ''):
        return Pizza(name=name, description=description, price=price)

    def get_preferences_page(self, user_id: int, limit: int, offset: int):
        pizzas_list = self.get_all()
        pizzas_pref = {pizza.id: [0, pizza] for pizza in pizzas_list}

        orders_list = self.session.query(Order).filter_by(user_id=user_id)
        for order in orders_list:
            month_ago = (
                datetime.now() - order.created_at
            ).total_seconds() / 60 / 60 / 24 // 30 + 1
            for order_item in order.order_items:
                pizzas_pref[order_item.pizza_id][0] -= \
                    order_item.quantity / month_ago

        pizzas_pref_list = [
            [
                pizza_id,
                pair[0],
                pair[1]
            ] for pizza_id, pair in pizzas_pref.items()
        ]
        pizzas_pref_list.sort(key=lambda x: (x[1], x[0]))

        print(pizzas_pref_list)

        return [pizza[2] for pizza in pizzas_pref_list][offset:offset + limit]
