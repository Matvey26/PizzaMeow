from .repository import Repository
from .models import User, Order, OrderStatusEnum, PaymentMethodEnum
from .payment_repository import PaymentRepository
from datetime import datetime

payment_repository = PaymentRepository()


class OrderRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Order)

    def create(self, user: User, delivery_cost: float, address: str, pickuptime: datetime):
        """Создаёт заказ из корзины по указанному пользователю, а также связанный с ним платёж."""
        new_order = Order(user=user, total_price=user.cart.total_price + delivery_cost, address=address, pickup_time=pickuptime)

        from .order_item_repository import OrderItemRepository
        order_item_repository = OrderItemRepository()

        for cart_item in user.cart.cart_items:
            order_item_repository.create(order=new_order, cart_item=cart_item)
        
        return new_order
    
    def get_page_by_user(self, user: User, limit: int, offset: int):
        return tuple(self.session.query(Order).filter_by(user_id=user.id).offset(offset).limit(limit).all())
    
    def change_status(self, order: Order, new_status: int):
        order.status = OrderStatusEnum(new_status)
        self.session.commit()

    def is_invalid(self, order: Order) -> list:
        invalid_fields = []
        return invalid_fields
