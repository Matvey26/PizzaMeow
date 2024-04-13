from .repository import Repository
from .models import User, Cart, CartItem


class CartRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Cart)

    def create_cart(self, user : User):
        new_cart = Cart(user_id=user.id)
        self.session.add(new_cart)
        self.session.commit(new_cart)

    def get_cart(self, user : User):
        return self.session.query(Cart).filter_by(user=user).first()

    def delete_cart(self, cart : Cart):
        deleted = self.session.delete(cart)
        self.session.commit()
        return deleted

    def add_item(self, cart : Cart, *items : CartItem):
        for item in items:
            item.cart_id = cart.id
            cart.order_items.append(item)
            self.session.commit(item)
        self.session.commit(cart)

    def delete_item(self, cart : Cart, *items : CartItem):
        for item in items:
            cart.order_items.remove(item)
        self.session.commit(cart)

    def clear_cart(self, cart : Cart):
        cart.order_items.clear()
        self.session.commit(cart)

    def get_items(self, cart : Cart):
        return cart.order_items
