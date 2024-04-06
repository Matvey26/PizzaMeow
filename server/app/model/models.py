import enum
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.database import Base


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
    cart = relationship('Cart', back_populates='user', uselist=False)
    payments = relationship('Payment', back_populates='user')

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'


class OrderCartMixin:
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)


class Order(OrderCartMixin, Base):
    __tablename__ = 'orders'

    status = sa.Column(sa.Enum(StatusEnum), nullable=False)

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    payment = relationship('Payment', back_populates='order')


class Cart(OrderCartMixin, Base):
    __tablename__ = 'carts'

    user = relationship('User', back_populates='cart')
    order_items = relationship('OrderItem', back_populates='cart')


class OrderItemTopping(Base):
    __tablename__ = 'order_item_toppings'

    order_item_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('order_items.id'),
        primary_key=True
    )
    topping_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('toppings.id'),
        primary_key=True
    )


class CartItemTopping(Base):
    __tablename__ = 'cart_item_toppings'

    order_item_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('cart_items.id'),
        primary_key=True
    )
    topping_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('toppings.id'),
        primary_key=True
    )


class OrderCartItemMixin:
    id = sa.Column(sa.Integer, primary_key=True)
    pizza_id = sa.Column(sa.Integer, sa.ForeignKey('Pizza'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)
    size = sa.Column(sa.Enum(PizzaSizeEnum))
    quantity = sa.Column(sa.Integer)


class OrderItem(Base):
    __tablename__ = 'order_items'

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


class CartItem(OrderCartItemMixin, Base):
    __tablename__ = 'cart_items'

    order_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('carts.id'),
        nullable=False
    )

    cart = relationship('Cart', back_populates='cart_items')
    pizza = relationship('Pizza', back_populates='_cart_items')
    toppings = relationship(
        argument='Topping',
        secondary='cart_item_toppings',
        back_populates='_cart_items'
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

    # Не следует использовать этот атрибут вне класса
    _cart_items = relationship(
        argument='CartItem',
        secondary='cart_item_toppings',
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
    _cart_items = relationship('CartItem', back_populates='pizza')


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
