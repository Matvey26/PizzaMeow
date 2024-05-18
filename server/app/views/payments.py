from . import payment_repository
from flask import abort


def confirm_payment(token):
    from ..utils.auth import decode_token
    token = decode_token(token)
    payment_id = int(token['sub'])
    payment = payment_repository.get(payment_id)
    if payment is None:
        abort(500, 'Токен недействителен.')
    payment_repository.mark_as_paid(payment)
    payment_repository.save(payment)
    