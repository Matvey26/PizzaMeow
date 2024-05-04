from ..model.pizzeria_repository import PizzeriaRepository
from ..model.order_repository import OrderRepository
from ..model.models import PaymentStatusEnum, OrderStatusEnum
import random
import os

pizzeria_repository = PizzeriaRepository()
order_repository = OrderRepository()


def generate_payment_url(id, amount):
    from .auth import generate_confirmation_url
    return generate_confirmation_url(str(id), os.environ['SERVER_URL'] + 'api/payments/confirm', 'payment_confirmation_token')


def calculate_delivery_cost(address):
    if pizzeria_repository.is_pizzeria_address(address):
        return 0

    return random.randint(50, 300)