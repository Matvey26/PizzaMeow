from server.database.fakedatabase import PIZZAS


def get_pizzas_page(offset, limit):
    return PIZZAS[offset:offset + limit]

