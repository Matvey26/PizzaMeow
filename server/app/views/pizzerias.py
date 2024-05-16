from . import pizzeria_repository


def get_addresses(address=None):
    pizzerias = [] 
    if address is None:
        pizzerias = pizzeria_repository.get_all()
    else:
        pizzerias = pizzeria_repository.get_nearest(address)
    ret = []
    for pizzeria in pizzerias:
        ret.append(pizzeria.address)
    
    return ret