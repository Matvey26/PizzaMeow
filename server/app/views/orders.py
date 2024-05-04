from . import user_repository
from . import order_repository, order_item_repository


def get_orders_page(limit: str, offset: str, user: str, token_info: dict):
    user_id = int(user)
    user = user_repository.get(user_id)
    page = order_repository.get_page_by_user(user=user, limit=limit, offset=offset)
    ret = []
    for order in page:
        data = order.serialize()
        data['order_items'] = []
        for order_item in order.order_items:
            data['order_items'].append(order_item.serialize())
    return ret


def order_by_id(id: int, user: str, token_info: dict):
    order_id = id
    user_id = int(user)