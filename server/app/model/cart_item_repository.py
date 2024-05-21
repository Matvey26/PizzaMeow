from .repository import Repository
from .models import CartItem, Pizza, PizzaSizeEnum, PizzaDoughEnum

conv_size_enum = {
    0: 'small',
    1: 'medium',
    2: 'large',
    'small': 'small',
    'medium': 'medium',
    'large': 'large'
}

conv_dough_enum = {
    0: 'thin',
    1: 'classic',
    'thin': 'thin',
    'classic': 'classic'
}


class CartItemRepository(Repository):
    def __init__(self):
        Repository.__init__(self, CartItem)

    def create(
        self,
        pizza: Pizza,
        total_price: float,
        quantity: int = 1,
        size: int = 1,
        dough: int = 1
    ) -> CartItem:

        size = conv_size_enum[size]
        dough = conv_dough_enum[dough]

        return CartItem(
            pizza=pizza,
            total_price=total_price,
            size=PizzaSizeEnum(size),
            quantity=quantity,
            dough=PizzaDoughEnum(dough)
        )

    def is_invalid(self, model: CartItem) -> list:
        invalid_fields = []
        return invalid_fields

    def delete(self, cart_item: CartItem):
        cart_item.cart.total_price -= cart_item.total_price
        deleted = self.session.delete(cart_item)
        self.session.commit()

        return deleted
