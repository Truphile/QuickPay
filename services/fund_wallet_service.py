def fund_wallet(user, amount):
    response=Initiate_paystack_payment(user,amount)
    deposit_notification(user,amount)
    return response