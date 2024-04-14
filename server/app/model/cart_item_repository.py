from .repository import Repository
from .models import CartItem, Pizza, PizzaSizeEnum


class CartItemRepository(Repository):
    def __init__(self):
        Repository.__init__(self, CartItem)

    def create(self, pizza: Pizza, total_price: float, size: PizzaSizeEnum, quantity: int) -> CartItem:
        return CartItem(
            pizza=pizza,
            total_price=total_price,
            size=size,
            quantity=quantity
        )
