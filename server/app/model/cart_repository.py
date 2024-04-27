from .repository import Repository
from .models import User, Cart, CartItem


class CartRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Cart)

    def create(self, user : User):
        return Cart(user_id=user.id, total_price=0)

    def get_by_user(self, user: User):
        result = self.session.query(Cart).filter_by(user_id=user.id).first()
        if result is None:
            result = self.create(user)  # корзина автоматически привязывается к пользователю
            self.save(result)
        return result

    def add_item(self, cart: Cart, *items: CartItem):
        sum_price = 0
        for item in items:
            sum_price += item.total_price
        cart.cart_items.extend(items)
        cart.total_price += sum_price
        self.session.commit()

    def clear(self, cart : Cart):
        for item in cart.cart_items:
            self.session.delete(item)
        self.session.commit()

    def get_items(self, cart: Cart):
        return cart.cart_items

    def is_invalid(self, model: Cart) -> list:
        invalid_fields = []
        return invalid_fields