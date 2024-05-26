from .repository import Repository
from .models import OrderItem, Order, CartItem
from .models import OrderItemIngredient


class OrderItemRepository(Repository):
    def __init__(self):
        Repository.__init__(self, OrderItem)

    def create(self, order: Order, cart_item: CartItem):
        """Создаёт позицию заказа из позиции корзины.
        """
        new_order_item = OrderItem(
            order=order,
            pizza=cart_item.pizza,
            total_price=cart_item.total_price,
            size=cart_item.size,
            quantity=cart_item.quantity,
            dough=cart_item.dough,
        )

        for cart_item_ingredient in cart_item.ingredients:
            order_item_ingredient = OrderItemIngredient(
                order_item_id=new_order_item.id,
                ingredient_id=cart_item_ingredient.ingredient_id,
                quantity=cart_item_ingredient.quantity
            )
            self.session.add(order_item_ingredient)

        return new_order_item

    def copy(self, order: Order, order_item: OrderItem):
        return OrderItem(
            order=order,
            pizza=order_item.pizza,
            total_price=order_item.total_price,
            size=order_item.size,
            quantity=order_item.quantity,
            dough=order_item.dough,
            toppings=order_item.toppings
        )
