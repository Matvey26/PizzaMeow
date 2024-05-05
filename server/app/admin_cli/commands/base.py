from ...model import CartRepository
from ...model import CartItemRepository
from ...model import OrderRepository
from ...model import OrderItemRepository
from ...model import UserRepository
from ...model import PaymentRepository
from ...model import PizzaRepository


class Base:
    """Базовая команда"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        self.repositories = {
            'user': UserRepository(),
            'pizza': PizzaRepository(),
            'payment': PaymentRepository(),
            'order': OrderRepository(),
            'order_item': OrderItemRepository(),
            'cart': CartRepository(),
            'cart_item': CartItemRepository(),
        }

    def run(self):
        raise NotImplementedError('You must implement the run() method!')
