from .repository import Repository
from .models import Cart, CartItem


class CartRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Cart)
    
    