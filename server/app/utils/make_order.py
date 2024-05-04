def generate_payments_url(price):
    return 'https://clck.ru/3AT7yu'


def calculate_delivery_cost(address):
    from ..model.pizzeria_repository import PizzeriaRepository
    pizzeria_repository = PizzeriaRepository()
    if pizzeria_repository.is_pizzeria_address(address):
        return 0
    
    import random
    return random.randint(50, 300)