from .repository import Repository
from .models import OrderItem, Order, Cart, CartItem, Pizza, PizzaSizeEnum


class OrderItemRepository(Repository):
    def __init__(self):
        Repository.__init__(self, OrderItem)

    def create(self, order: Order, cart_item: CartItem):
        """Создаёт позицию заказа из позиции корзины.
        """
        return OrderItem(
            order=order,
            pizza=cart_item.pizza,
            total_price=cart_item.total_price,
            size=cart_item.size,
            quantity=cart_item.quantity,
            toppings=cart_item.toppings
        )

    def copy(self, order: Order, order_item: OrderItem):
        return OrderItem(
            order=order,
            pizza=order_item.pizza,
            total_price=order_item.total_price,
            size=order_item.size,
            quantity=order_item.quantity,
            toppings=order_item.toppings
        )

    def is_invalid(self, order_item: OrderItem) -> list:
        invalid_fields = []
        return invalid_fields
