from . import user_repository, cart_repository
from . import order_repository, payment_repository
from flask import abort
import asyncio


def get_orders_page(limit: str, offset: str, user: str, token_info: dict):
    user_id = int(user)
    user = user_repository.get(user_id)
    if user is None:
        abort(401, 'Токен недействителен, либо учетная запись удалена')
    page = order_repository.get_page_by_user(user=user, limit=limit, offset=offset)
    
    return order_repository.serialize(*page)


def get_order_by_id(id: int, user: str, token_info: dict):
    order_id = id
    user_id = int(user)
    order = order_repository.get_by_user_and_order_ids(user_id=user_id, order_id=order_id)
    if order is None:
        abort(400, 'Вы не делали такого заказа, проверьте указанный ID')

    return order_repository.serialize(order)[0]


task_queue = asyncio.Queue()


async def create_order(user, token_info, body):
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

    # создаем асинхронную задачу на отмену заказа (точнее добавляем заказ в очередь)
    await task_queue.put(order.id)

    # отправляем ссылку для оплаты
    from ..utils.make_order import generate_payment_url
    if payment_method == 'online':
        return {
            'payment_url': generate_payment_url(payment.id, payment.amount)
        }


# Этот фоновый процесс отвечает за выполнение задач на отмену заказов,
# если те не были оплачены в течение 15 минут
async def process_queue():
    from ..utils.make_order import cancel_order_if_not_paid
    while True:
        order_id = await task_queue.get()
        order = order_repository.get(order_id)
        task = cancel_order_if_not_paid(order)
        await task


# запускаем процесс обработки очереди в фоновом режиме
asyncio.create_task(process_queue())