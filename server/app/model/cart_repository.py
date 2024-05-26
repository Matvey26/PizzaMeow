from .repository import Repository
from .models import User, Cart, CartItem
from .cart_item_ingredients_repository import CartItemIngredientRepository

cart_item_ingredients_repository = CartItemIngredientRepository()


class CartRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Cart)

    def create(self, user: User):
        return Cart(user_id=user.id, total_price=0)

    def get_by_user(self, user: User):
        result = self.session.query(Cart).filter_by(user_id=user.id).first()
        if result is None:
            # корзина автоматически привязывается к пользователю
            result = self.create(user)
            self.save(result)
        return result

    def add_item(self, cart: Cart, *items: CartItem):
        sum_price = 0
        for item in items:
            sum_price += item.total_price
        cart.cart_items.extend(items)
        cart.total_price += sum_price
        self.session.commit()

    def clear(self, cart: Cart):
        for item in cart.cart_items:
            self.session.delete(item)
        cart.total_price = 0
        self.session.commit()

    def get_items(self, cart: Cart):
        return cart.cart_items

    def serialize(self, cart: Cart) -> dict:
        """Сериализует корзину.
        Иначе говоря представляет корзину в виде списка её элементов.
        Все поля, содержащие enum переводятся в текст.
        """

        serialized = {
            'id': cart.id,
            'total_price': cart.total_price,
            'cart_items': []
        }
        for cart_item in cart.cart_items:
            data = cart_item.serialize()
            data['pizza_name'] = cart_item.pizza.name
            data['ingredients'] = cart_item_ingredients_repository.serialize(
                *cart_item.ingredients
            )
            print(data)
            serialized['cart_items'].append(data)

        return serialized
