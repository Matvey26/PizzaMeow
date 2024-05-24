import enum
import sqlalchemy as sa
from ..database import Base, engine
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields


class CustomSQLAlchemyAutoSchema(SQLAlchemyAutoSchema):
    def _get_field(self, column, *args, **kwargs):
        if isinstance(column.type, sa.Enum):
            return fields.Method('serialize', deserialize=fields.Str())
        return super()._get_field(column, *args, **kwargs)


class Model:
    """Класс Model объявляет метод serialize(),
    который сериализует данные модели.
    """

    def create_schema(self) -> None:
        """Создаёт marshmallow схему для (де)сериализации."""
        class Meta(object):
            model = self.__class__
            # include_relationships = True
            load_instance = True
            include_fk = True

        ModelSchema = type(
            f'{self.__class__.__name__}Schema',
            (CustomSQLAlchemyAutoSchema,),
            {'Meta': Meta}
        )

        self.model_schema = ModelSchema()

    def serialize(self) -> dict:
        """Сериализует аттрибуты объекта в словарь."""
        if not hasattr(self, 'model_schema'):
            self.create_schema()

        data = self.model_schema.dump(self)

        # Сериализуем Enum поля
        for key, value in data.items():
            if isinstance(value, enum.Enum):
                data[key] = value.serialize()

        return data

    def remove_session(self):
        """Удаляет объект из текущей сессии."""

        session = inspect(self).session
        if session:
            session.expunge(self)


class OrderStatusEnum(enum.Enum):
    PROCESS = 'process'  # обрабатывается, ещё начал готовиться
    COOKING = 'cooking'  # готовится
    EN_ROUTE = 'en_route'  # в пути (если доставка)
    READY_TO_PICKUP = 'ready_to_pickup'  # готов к выдаче (если самовывоз)
    DONE = 'done'  # заказ завершён
    CANCELLED = 'cancelled'  # заказ был отменён

    def serialize(self):
        return self.value


class PizzaSizeEnum(enum.Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'

    def serialize(self):
        return self.value


class PizzaDoughEnum(enum.Enum):
    THIN = 'thin'
    CLASSIC = 'classic'

    def serialize(self):
        return self.value


class PaymentMethodEnum(enum.Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'

    def serialize(self):
        return self.value


class PaymentStatusEnum(enum.Enum):
    PENDING = 0
    PAID = 1

    def serialize(self):
        return self.value


class UserConfirmEnum(enum.Enum):
    CONFIRMED = 'CONFIRMED'
    NOTCONFIRMED = 'NOTCONFIRMED'

    def serialize(self):
        return self.value


class User(Base, Model):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(150), nullable=False, unique=True)
    password = sa.Column(sa.String(100), nullable=False)
    firstname = sa.Column(sa.String(100), nullable=True)
    lastname = sa.Column(sa.String(100), nullable=True)
    phone_number = sa.Column(sa.String(20), nullable=True)
    address = sa.Column(sa.String(400), nullable=True)
    _confirmed = sa.Column(
        sa.Enum(UserConfirmEnum),
        default=UserConfirmEnum.NOTCONFIRMED
    )

    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan, save-update')
    cart = relationship('Cart', back_populates='user', uselist=False, cascade='all, delete-orphan, save-update')
    payments = relationship('Payment', back_populates='user', cascade='all, delete-orphan, save-update')

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'


class Order(Base, Model):
    __tablename__ = 'orders'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)
    delivery_price = sa.Column(sa.Float, default=0.)
    status = sa.Column(sa.Enum(OrderStatusEnum), default=OrderStatusEnum.PROCESS, nullable=False)
    address = sa.Column(sa.Text, nullable=False)
    pickup_time = sa.Column(sa.DateTime)
    created_at = sa.Column(sa.DateTime, server_default=func.now())

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan, save-update')
    payment = relationship('Payment', back_populates='order', cascade='all, delete-orphan, save-update', uselist=False)


class Cart(Base, Model):
    __tablename__ = 'carts'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)

    user = relationship('User', back_populates='cart')
    cart_items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan, save-update')


class Ingredient(Base, Model):
    __tablename__ = 'ingredients'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(150), nullable=False)
    description = sa.Column(sa.Text)
    price = sa.Column(sa.Float, nullable=False)


class CartItem(Base, Model):
    __tablename__ = 'cart_items'

    id = sa.Column(sa.Integer, primary_key=True)
    pizza_id = sa.Column(sa.Integer, sa.ForeignKey('pizzas.id'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)
    size = sa.Column(sa.Enum(PizzaSizeEnum))
    quantity = sa.Column(sa.Integer)
    dough = sa.Column(sa.Enum(PizzaDoughEnum))
    cart_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('carts.id'),
    )

    cart = relationship('Cart', back_populates='cart_items')
    pizza = relationship('Pizza', back_populates='_cart_items')
    ingredients = relationship('CartItemIngredient', back_populates='cart_item')

    def serialize(self) -> dict:
        """Сериализует аттрибуты объекта в словарь, включая ингредиенты."""
        data = super().serialize()
        data['ingredients'] = [{'id': ing.ingredient_id, 'quantity': ing.quantity} for ing in self.ingredients]
        return data


class CartItemIngredient(Base, Model):
    __tablename__ = 'cart_item_ingredients'

    id = sa.Column(sa.Integer, primary_key=True)
    cart_item_id = sa.Column(sa.Integer, sa.ForeignKey('cart_items.id'))
    ingredient_id = sa.Column(sa.Integer, sa.ForeignKey('ingredients.id'), nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)

    cart_item = relationship('CartItem', back_populates='ingredients')
    ingredient = relationship('Ingredient')


class OrderItem(Base, Model):
    __tablename__ = 'order_items'

    id = sa.Column(sa.Integer, primary_key=True)
    pizza_id = sa.Column(sa.Integer,sa.ForeignKey('pizzas.id'), nullable=False)
    total_price = sa.Column(sa.Float, nullable=False)
    size = sa.Column(sa.Enum(PizzaSizeEnum))
    quantity = sa.Column(sa.Integer)
    dough = sa.Column(sa.Enum(PizzaDoughEnum))
    order_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('orders.id'),
        nullable=False
    )

    order = relationship('Order', back_populates='order_items')
    pizza = relationship('Pizza', back_populates='_order_items')
    ingredients = relationship('OrderItemIngredient', back_populates='order_item')

    def serialize(self) -> dict:
        """Сериализует аттрибуты объекта в словарь, включая ингредиенты."""
        data = super().serialize()
        data['ingredients'] = [{'id': ing.ingredient_id, 'quantity': ing.quantity} for ing in self.ingredients]
        return data


class OrderItemIngredient(Base, Model):
    __tablename__ = 'order_item_ingredients'

    id = sa.Column(sa.Integer, primary_key=True)
    cart_item_id = sa.Column(sa.Integer, sa.ForeignKey('order_items.id'), nullable=False)
    ingredient_id = sa.Column(sa.Integer, sa.ForeignKey('ingredients.id'), nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)

    order_item = relationship('OrderItem', back_populates='ingredients')
    ingredient = relationship('Ingredient')


class Pizza(Base, Model):
    __tablename__ = 'pizzas'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(150), nullable=False)
    description = sa.Column(sa.Text)
    price = sa.Column(sa.Float, nullable=False)

    # Не следует использовать этот атрибут вне класса
    _order_items = relationship('OrderItem', back_populates='pizza')
    _cart_items = relationship('CartItem', back_populates='pizza')


class Payment(Base, Model):
    __tablename__ = 'payments'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    order_id = sa.Column(sa.Integer, sa.ForeignKey('orders.id'), nullable=False)
    payment_method = sa.Column(sa.Enum(PaymentMethodEnum), nullable=False)
    amount = sa.Column(sa.Float, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=func.now())
    payment_date = sa.Column(sa.DateTime)
    payment_status = sa.Column(sa.Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING)

    order = relationship('Order', back_populates='payment', uselist=False)
    user = relationship('User', back_populates='payments', uselist=False)


class Pizzeria(Base, Model):
    __tablename__ = 'pizzerias'

    id = sa.Column(sa.Integer, primary_key=True)
    address = sa.Column(sa.Text, nullable=False, unique=True)


# Создаём таблицы
Base.metadata.create_all(engine)
