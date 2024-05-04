from . import user_repository, cart_repository
from . import order_repository, payment_repository
from flask import abort


def get_orders_page(limit: str, offset: str, user: str, token_info: dict):
    user_id = int(user)
    user = user_repository.get(user_id)
    if user is None:
        abort(401, 'Токен недействителен, либо учетная запись удалена')

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


def create_order(user, token_info, body):
    user_id = int(user)
    user = user_repository.get(user_id)
    if user is None:
        abort(401, 'Токен недействителен, либо учётная запись удалена')
    if not user_repository.is_confirmed(user):
        abort(401, 'Почта пользователя не подтверждена')

    # -------- ПОЛУЧАЕМ ДАННЫЕ --------

    # адрес назначения заказа
    address = body.get('address', '')  # TODO: добавить проверку валидности адреса

    # время желаемого получения заказа
    from datetime import datetime
    pickup_time = body.get('pickup_time', '')  # TODO: добавить проверку валидности времени получения заказа
    try:
        pickup_time = datetime.fromisoformat(pickup_time)
    except Exception:
        abort(400, 'Неверный формат даты')

    # метод оплаты
    payment_method = body.get('payment_method', '')
    if payment_method not in ['online', 'offline']:
        abort(400, 'Указан неверный метод оплаты')

    # ---------- ФОРМИРУЕМ ЗАКАЗ -------------

    # создаём заказ
    from ..utils.make_order import calculate_delivery_cost
    order = order_repository.create(
        user=user,
        delivery_cost=calculate_delivery_cost(address),
        address=address,
        pickuptime=pickup_time
    )
    order_repository.save(order)

    # создаём платёж
    payment = payment_repository.create(order=order, payment_method=payment_method)
    payment_repository.save(payment)

    # очищаем корзину
    cart_repository.clear(user.cart)

    # отправляем ссылку для оплаты
    from ..utils.make_order import generate_payment_url
    if payment_method == 'online':
        return {
            'payment_url': generate_payment_url(payment.id, payment.amount)
        }
