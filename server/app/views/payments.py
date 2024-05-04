from . import payment_repository


def confirm_payment(payment_confirmation_token):
    from ..utils.auth import decode_token
    token = decode_token(payment_confirmation_token)
    payment_id = int(token['sub'])
    payment = payment_repository.get(payment_id)
    payment_repository.mark_as_paid(payment)
    
    