from .repository import Repository
from .models import Payment, Order, PaymentMethodEnum, PaymentStatusEnum


class PaymentRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Payment)

    def create(self, order: Order, payment_method: str):
        return Payment(
            user=order.user,
            order=order,
            payment_method=PaymentMethodEnum(payment_method),
            amount=order.total_price,
        )

    def mark_as_paid(self, payment: Payment):
        payment.payment_status = PaymentStatusEnum.PAID
