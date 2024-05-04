from .repository import Repository
from .models import User, Order, OrderItem, Cart, StatusEnum, Payment

class OrderRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Order)

    # def create_order(self, user: User, total_price: float, *order_items: OrderItem):
    #     new_order = Order(user_id=user.id, total_price=total_price, status=0)
    #     for order_item in order_items:
    #         order_item.order_id = new_order.id
    #         new_order.order_items.append(order_item)
    #     self.session.add(new_order)
    #     self.session.commit(new_order)

    def create(self, user: User, cart: Cart):
        """Создаёт заказ из корзины."""
        new_order = Order(user=user, total_price=cart.total_price)

        from .order_item_repository import OrderItemRepository
        order_item_repository = OrderItemRepository()

        for cart_item in cart.cart_items:
            order_item_repository.create_from_cart_item(order=new_order, cart_item=cart_item)
        
        return new_order
    
    def change_status(self, order: Order, new_status: int):
        order.status = StatusEnum(new_status)
        self.session.commit()

    def is_invalid(self, order: Order) -> list:
        invalid_fields = []
        return invalid_fields
