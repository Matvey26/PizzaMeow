from .repository import Repository
from .models import OrderItem, Order, Cart, CartItem, Pizza, PizzaSizeEnum

class OrderItemRepository(Repository):
    def __init__(self):
        Repository.__init__(self, OrderItem)

    # def create(self, order: Order, pizza: Pizza, total_price: float, size: PizzaSizeEnum, quantity: int):
    #     new_order_item = OrderItem(
    #         pizza_id=pizza.id,
    #         total_price=total_price,
    #         size=size,
    #         quantity=quantity,
    #         order_id=order.id
    #     )
    #     self.session.add(new_order_item)
    #     self.session.commit(new_order_item)
    
    def create(self, order: Order, cart_item: CartItem):
        """Создаёт позицию заказа из позиции корзины.
        """
        return OrderItem(
            order=order,
            pizza = cart_item.pizza,
            total_price = cart_item.total_price,
            size = cart_item.size,
            quantity = cart_item.quantity,
            toppings = cart_item.toppings
        )

    def is_invalid(self, order_item: OrderItem) -> list:
        invalid_fields = []
        return invalid_fields