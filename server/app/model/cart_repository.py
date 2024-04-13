from .repository import Repository
from .models import Cart, CartItem


class CartRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Cart)

    def create_cart(self, user : User):
        new_cart = Cart(user=user, order_items=[])
        self.session.add(new_cart)
        self.session.commit(new_cart)

    def get_cart(self, user : User):
        return self.session.query(Cart).filter_by(user=self.user).first()

    def delete_cart(self, cart : Cart):
        deleted = self.session.delete(cart)
        self.session.commit()

    def add_item(self, cart : Cart, item : CartItem):
        cart.order_items.append(item)
        self.session.commit(cart)

    def delete_item(self, cart : Cart, item : CartItem):
        cart.order_items.remove(item)
        self.session.commit(cart)

    def clear_cart(self, cart : Cart):
        cart.order_items.clear()
        self.session.commit(cart)

    def get_items(self, Cart : cart):
        return cart.order_items
