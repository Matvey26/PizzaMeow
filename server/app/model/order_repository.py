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

    def create_from_cart(self, user: User, cart: Cart):
        new_order = Order(user=user, total_price=cart.total_price)

        from .order_item_repository import OrderItemRepository
        order_item_repository = OrderItemRepository(self.session)

        for cart_item in cart.cart_items:
            order_item_repository.create_from_cart_item(order=new_order, cart_item=cart_item)
        
        return new_order
    
    def change_status(self, order: Order, new_status: StatusEnum):
        order.status = new_status
        self.session.commit(order)

