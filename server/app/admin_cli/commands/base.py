from ...model import UserRepository, PizzaRepository
from ...model import CartRepository, CartItemRepository
from ...model import OrderRepository, OrderItemRepository
from ...model import PizzeriaRepository, PaymentRepository
from ...model import IngredientRepository


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
            'order_item_ingredient'
            'cart': CartRepository(),
            'cart_item': CartItemRepository(),
            'ingredient': IngredientRepository(),
            'pizzeria': PizzeriaRepository()
        }

    def run(self):
        raise NotImplementedError('You must implement the run() method!')
