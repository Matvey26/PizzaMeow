import json

PATH = 'server/database/pizzas.json'

with open(PATH, 'r') as db:
    PIZZAS = json.load(db)

def get_pizzas_page(offset, limit):
    return PIZZAS[offset:offset + limit]