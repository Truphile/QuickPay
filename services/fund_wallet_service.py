from wallet.services.fund_wallet import initiate_paystack_payment
from notification.services import deposit_notification

def fund_wallet(user, amount):
    response=initiate_paystack_payment(user,amount)
    deposit_notification(user,amount)
    return response