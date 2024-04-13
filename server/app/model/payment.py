from .repository import Repository
from .models import Payment, User, Order
import datetime

class PaymentRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Payment)

    def create_payment(self, user : User, order : Order, payment_method, amount):
       new_payment = Payment(user_id=user.id, order_id=order.id, payment_method=payment_method, amount=amount, payment_date=datetime.datetime.now())
       order.payment = new_payment
       user.payments.append(new_payment)
       self.session.add(new_payment)
       self.session.commit(new_payment, order.payment, user.payments)

    def get_payment(self, payment : Payment):
        return self.session.query(Payment).filter_by(id=payment.id).first()

    def get_payment_id(self, id : int):
        return self.session.query(Payment).filter_by(id=id).first()

    def get_user_payments(self, user : User):
        return self.session.query(Payment).filter_by(user_id=user.id).all()

    def get_order_payment(self, order : Order):
        return self.session.query(Payment).filter_by(order_id=order.id).first()

    def get_all_payments(self):
        return self.session.query(Payment).filter_by(order_id=order.id).first()

    def delete_payment(self, payment : Payment):
        deleted = self.session.delete(payment)
        payment
        self.session.commit()
        return deleted