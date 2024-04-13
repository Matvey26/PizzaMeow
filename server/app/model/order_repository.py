from .repository import Repository
from .models import User, Order, OrderItem

class OrderRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Order)

    def create_order(self, user : User, total_price : float, *order_items : OrderItem):
        new_order = Order(user_id=user.id, total_price=total_price, status=0)
        for order_item in order_items:
            order_item.order_id = new_order.id
            new_order.order_items.append(order_item)
        self.session.add(new_order)
        self.session.commit(new_order)
    
    def change_status(self, order : Order, new_status):
        order.status = new_status
        self.session.commit(order)

    def delete_order(self, order : Order):
        for item in order.order_items:
            order.order_items.remove(item)
            self.session.delete(item)
        deleted = self.session.delete(order)
        self.session.commit()
        return deleted

    def get_user_orders(self, user : User):
        return self.session.query(Order).filter_by(user_id=user.id).all()

    def get_all_orders(self):
        return self.session.query(Order).all()

    def get_order(self, id : int):
        return self.session.query(Order).filter_by(id=id).first()

    def get_order_payment(self, order : Order):
        return self.session.query(Payment).filter_by(order_id=order.id).first()
