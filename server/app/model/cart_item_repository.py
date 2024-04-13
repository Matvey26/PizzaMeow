from .repository import Repository
from .models import CartItem, Pizza

class CartItemRepository(Repository):
    def __init__(self):
        Repository.__init__(self, CartItem)
    
    def create_cart_item(self, pizza : Pizza, total_price : float, size, quantity):
        new_cart_item = CartItem(pizza_id=pizza.id, total_price=total_price, size=size, quantity=quantity)
        self.session.add(new_cart_item)
        self.session.commit(new_cart_item)

    def get_cart_item(self, id : int):
        return self.session.query(CartItem).filter_by(id=id).first()

    def change_cart_item(self, cart_item : CartItem, new_pizza=None, new_price=None, new_size=None, new_quantity=None):
        if new_pizza:
            cart_item.pizza_id = new_pizza.cart_id
        if new_price:
            cart_item.total_price = new_price
        if new_size:
            cart_item.size = new_size
        if new_quantity:
            cart_item.quantity = new_quantity
        self.session.commit(cart_item)

    def get_cart_item(self, id : int):
        return self.session.query(CartItem).filter_by(id=id).first()

    def get_cart_items(self):
        return self.session.query(CartItem).all()

    def delete_cart_item(self, cart_item : CartItem):
        deleted = self.session.delete(cart_item)
        self.session.commit()
        return deleted
