from .repository import Repository
from .models import Payment, User, Order, PaymentMethodEnum
import datetime

class PaymentRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Payment)

    def create(self, order : Order, payment_method: str):
        return Payment(
            user=order.user,
            order=order,
            payment_method=PaymentMethodEnum(payment_method),
            amount=order.total_price,
        )

    def is_invalid(self, payment: Payment) -> list:
        invalid_fields = []
        return invalid_fields