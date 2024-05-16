from .repository import Repository
from .models import Pizzeria
from sqlalchemy import func

class PizzeriaRepository(Repository):
    def __init__(self):
        Repository.__init__(self, Pizzeria)
    
    def get_nearest(self, address: str):
        # Это неполноценное решение, просто заглушка.
        return self.session.query(Pizzeria).all()
    
    def is_pizzeria_address(self, address: str) -> bool:
        pizzeria = self.session.query(Pizzeria).filter_by(address=address).all()
        return pizzeria is not None
    
    def is_invalid(self, pizzeria: Pizzeria):
        invalid_fields = []
        return invalid_fields
    