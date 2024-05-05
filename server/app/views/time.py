import random


def get_delivery_time(address, user, token_info):
    return {
        'time': random.randint(10, 45)
    }


def get_cooking_time(user, token_info):
    return {
        'time': random.randint(10, 60)
    }