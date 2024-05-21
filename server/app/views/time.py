from typing import List


def get_delivery_time(address, user, token_info):
    return [
        ['2024-05-15T10:00:15.310793+00:00', '2024-05-15T13:00:15.310793+00:00'],
        ['2024-05-15T13:00:15.310793+00:00', '2024-05-15T16:00:15.310793+00:00'],
        ['2024-05-15T16:00:15.310793+00:00', '2024-05-15T19:00:15.310793+00:00']
    ]


def get_cooking_time(user, token_info):
    return [
        ['2024-05-15T10:00:15.310793+00:00', '2024-05-15T13:00:15.310793+00:00'],
        ['2024-05-15T13:00:15.310793+00:00', '2024-05-15T16:00:15.310793+00:00'],
        ['2024-05-15T16:00:15.310793+00:00', '2024-05-15T19:00:15.310793+00:00']
    ]


def is_valid_pickup_time(time_interval: List[str]) -> bool:
    return True


def is_valid_delivery_time(time_interval: List[str]) -> bool:
    return True
