from .repository import Repository
from .models import User, Order, OrderStatusEnum, PaymentMethodEnum
from .payment_repository import PaymentRepository
from datetime import datetime
from typing import List
from sqlalchemy import or_

payment_repository = PaymentRepository()

active_statuses = [
    OrderStatusEnum.PROCESS,
    OrderStatusEnum.COOKING,
    OrderStatusEnum.EN_ROUTE,
    OrderStatusEnum.READY_TO_PICKUP
]

completed_statuses = [
    OrderStatusEnum.DONE,
    OrderStatusEnum.CANCELLED
]


class OrderRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Order)

    def create(self, user: User, address: str, delivery_cost: float = 0):
        """Создаёт заказ из корзины по указанному пользователю."""
        new_order = Order(
            user=user,
            total_price=user.cart.total_price,
            delivery_price=delivery_cost,
            address=address
        )

        from .order_item_repository import OrderItemRepository
        order_item_repository = OrderItemRepository()

        for cart_item in user.cart.cart_items:
            order_item_repository.create(order=new_order, cart_item=cart_item)

        return new_order

    def copy(self, other: Order):
        new_order = Order(
            user=other.user,
            total_price=other.total_price,
            delivery_price=other.delivery_price,
            address=other.address
        )

        from .order_item_repository import OrderItemRepository
        order_item_repository = OrderItemRepository()

        for order_item in other.order_items:
            order_item_repository.copy(new_order, order_item)

        return new_order

    def get_page_by_user(self, user: User, limit: int, offset: int, active: bool, completed: bool):
        query = self.session.query(Order).filter_by(user_id=user.id)

        if active and not completed:
            query = query.filter(Order.status.in_(active_statuses))
        elif completed and not active:
            query = query.filter(Order.status.in_(completed_statuses))
        elif active and completed:
            query = query.filter(or_(Order.status.in_(active_statuses),
                                     Order.status.in_(completed_statuses)))

        answer = tuple(query.limit(limit).offset(offset).all())
        return answer

    def change_status(self, order: Order, new_status: int):
        order.status = OrderStatusEnum(new_status)
        self.session.commit()

    def is_invalid(self, order: Order) -> list:
        invalid_fields = []
        return invalid_fields

    def get_by_user_and_order_ids(self, user_id, order_id):
        return self.session.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()

    def serialize(self, *orders: Order) -> dict:
        serialized = []
        for order in orders:
            if not isinstance(order, Order):
                raise TypeError(
                    'В списке заказов найден экземпляр другого класса')
            data = order.serialize()
            data['order_items'] = []
            for order_item in order.order_items:
                data['order_items'].append(order_item.serialize())
            serialized.append(data)

        return serialized

    def mark_as_cancelled(self, order: Order):
        order.status = OrderStatusEnum.CANCELLED
