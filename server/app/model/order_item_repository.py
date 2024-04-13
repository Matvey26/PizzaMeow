from .repository import Repository
from .models import OrderItem, Order, Pizza

class OrderItemRepository(Repository):
    def __init__(self):
        Repository.__init__(self, OrderItem)

    def create_order_item(self, pizza : Pizza, total_price : float, size, quantity : int, order : Order):
        new_order_item = OrderItem(pizza_id=pizza.id, total_price=total_price, size=size, quantity=quantity, order_id=order.id)
        self.session.add(new_order_item)
        self.session.commit(new_order_item)

    def change_order_item(self, order_item : OrderItem, new_pizza=None, new_price=None, new_size=None, new_quantity=None, new_order=None):
        if new_pizza:
            order_item.pizza_id = new_pizza.id
        if new_price:
            order_item.total_price = new_price
        if new_size:
            order_item.new_size = new_size
        if new_quantity:
            order_item.new_quantity = new_quantity
        if new_order:
            order_item.order_id = new_order.id
        self.session.commit(order_item)

    def get_order_item(self, id : int):
        return self.session.query(OrderItem).filter_by(id=id).first()
    
    def get_order_items(self):
        return self.session.query(OrderItem).all()

    def delete_order_item(self, order_item : OrderItem):
        deleted = self.session.delete(order_item)
        self.session.commit()
        return deleted








class OrderItem(Base, Model):
    __tablename__ = 'order_items'


    id = sa.Column(sa.Integer, primary_key=True)
    pizza_id = sa.Column(sa.Integer, sa.ForeignKey('pizzas.id'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)
    size = sa.Column(sa.Enum(PizzaSizeEnum))
    quantity = sa.Column(sa.Integer)
    order_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('orders.id'),
        nullable=False
    )

    order = relationship('Order', back_populates='order_items')
    pizza = relationship('Pizza', back_populates='_order_items')
    toppings = relationship(
        argument='Topping',
        secondary='order_item_toppings',
        back_populates='_order_items'
    )