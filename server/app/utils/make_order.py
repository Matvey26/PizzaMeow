from ..model.pizzeria_repository import PizzeriaRepository
from ..model.order_repository import OrderRepository
from ..model.payment_repository import PaymentRepository
from ..model.models import PaymentStatusEnum, OrderStatusEnum
from ..model.models import Order
import random
import os
import asyncio

pizzeria_repository = PizzeriaRepository()
order_repository = OrderRepository()
payment_repository = PaymentRepository()


def generate_payment_url(id, amount):
    from .auth import generate_confirmation_url
    return generate_confirmation_url(str(id), os.environ['SERVER_URL'] + 'api/payments/confirm')


def calculate_delivery_cost(address):
    return random.randint(50, 300)


async def cancel_order_if_not_paid(order: Order):
    await asyncio.sleep(15 * 60)
    if order.payment.payment_status == PaymentStatusEnum.PENDING:
        order_repository.mark_as_cancelled(order)