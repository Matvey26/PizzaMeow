from ..model import UserRepository, PizzaRepository
from ..model import CartRepository, CartItemRepository
from ..model import OrderRepository, OrderItemRepository
from ..model import PizzeriaRepository, PaymentRepository
from ..model import IngredientRepository

user_repository = UserRepository()
pizza_repository = PizzaRepository()
cart_repository = CartRepository()
cart_item_repository = CartItemRepository()
order_repository = OrderRepository()
order_item_repository = OrderItemRepository()
pizzeria_repository = PizzeriaRepository()
payment_repository = PaymentRepository()
ingredient_repository = IngredientRepository()
