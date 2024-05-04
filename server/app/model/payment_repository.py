from .repository import Repository
from .models import Payment, User, Order, PaymentMethodEnum
import datetime

class PaymentRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Payment)

    def create(self, user : User, order : Order, payment_method: int, amount: float):
        return Payment(
            user=user,
            order=order,
            payment_method=PaymentMethodEnum(payment_method),
            amount=amount,
            payment_date=datetime.datetime.now()
        )

    def is_invalid(self, payment: Payment) -> list:
        invalid_fields = []
        return invalid_fields