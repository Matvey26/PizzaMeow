from .repository import Repository
from .models import CartItemIngredient


class CartItemIngredientRepository(Repository):
    def __init__(self):
        Repository.__init__(self, CartItemIngredient)

    def create(self, ingredient_id: int, quantity: int):
        return CartItemIngredient(
            ingredient_id=ingredient_id,
            quantity=quantity
        )

    def serialize(self, *cart_item_ingredients: CartItemIngredient):
        serialized = []
        for cart_item_ingredient in cart_item_ingredients:
            data = {
                'id': cart_item_ingredient.ingredient_id,
                'quantity': cart_item_ingredient.quantity
            }
            serialized.append(data)
        return serialized
