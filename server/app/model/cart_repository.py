from .repository import Repository
from .models import User, Cart, CartItem


class CartRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Cart)

    def create(self, user : User):
        return Cart(user=user)

    def get_by_user_id(self, user_id: int):
        return self.session.query(Cart).filter_by(user_id=user_id).first()

    def add_item(self, cart: Cart, *items: CartItem):
        cart.cart_items.extend(items)
        self.session.commit(cart)

    def clear(self, cart : Cart):
        for item in cart.cart_items:
            self.session.delete(item)
        self.session.commit()

    def get_items(self, cart: Cart):
        return cart.cart_items
