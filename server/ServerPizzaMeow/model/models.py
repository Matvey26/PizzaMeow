import enum
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ServerPizzaMeow.database import Base


class StatusEnum(enum.Enum):
    RECEIVED = 0
    BEING_PREPARED = 1
    COOKED = 2
    EN_ROUTE = 3
    READY_FOR_PICKUP = 4
    DONE = 5


class PizzaSizeEnum(enum.Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class PaymentMethodEnum(enum.Enum):
    CASH = 0
    CARD_ONLINE = 1
    CARD_UPON_RECEIPT = 2


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(150), nullable=False)
    password = sa.Column(sa.String(100), nullable=False)
    firstname = sa.Column(sa.String(100), nullable=True)
    lastname = sa.Column(sa.String(100), nullable=True)
    phone_number = sa.Column(sa.String(20), nullable=True)
    address = sa.Column(sa.String(400), nullable=True)

    orders = relationship('Order', back_populates='user')
    payments = relationship('Payment', back_populates='user')

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'


class Order(Base):
    __tablename__ = 'orders'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    status = sa.Column(sa.Enum(StatusEnum), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    payment = relationship('Payment', back_populates='order')


class OrderItemTopping(Base):
    __tablename__ = 'order_item_toppings'

    order_item_id = sa.Column(sa.Integer, sa.ForeignKey(
        'order_items.id'), primary_key=True)
    topping_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('toppings.id'),
        primary_key=True
    )


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = sa.Column(sa.Integer, primary_key=True)
    order_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('orders.id'),
        nullable=False
    )
    pizza_id = sa.Column(sa.Integer, sa.ForeignKey('Pizza'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)
    size = sa.Column(sa.Enum(PizzaSizeEnum))
    quantity = sa.Column(sa.Integer)

    order = relationship('Order', back_populates='order_items')
    pizza = relationship('Pizza', back_populates='_order_items')
    toppings = relationship(
        argument='Topping',
        secondary='order_item_toppings',
        back_populates='_order_items'
    )


class Topping(Base):
    __tablename__ = 'toppings'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(150), nullable=False)
    description = sa.Column(sa.Text)
    price = sa.Column(sa.Float, nullable=False)

    # Не следует использовать этот атрибут вне класса
    _order_items = relationship(
        argument='OrderItem',
        secondary='order_item_toppings',
        back_populates='toppings'
    )


class Pizza(Base):
    __tablename__ = 'pizzas'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(150), nullable=False)
    description = sa.Column(sa.Text)
    price = sa.Column(sa.Float, nullable=False)

    # Не следует использовать этот атрибут вне класса
    _order_items = relationship('OrderItem', back_populates='pizza')


class Payment(Base):
    __tablename__ = 'payments'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders'), nullable=False)
    payment_method = sa.Column(sa.Enum(PaymentMethodEnum), nullable=False)
    amount = sa.Column(sa.Float, nullable=False)
    payment_date = sa.Column(sa.DateTime, nullable=False)

    order = relationship('Order', back_populates='payment', uselist=False)
    user = relationship('User', back_populates='payments', uselist=False)
