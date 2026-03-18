import notification
from notification.models import Notification
from django.core.mail import send_mail

from wallet.models import Wallet


def create_notification(user):
    notification = Notification.objects.create(user=user,
                                message=f"""
                                Hi {user.first_name} Welcome to Quickpay!
                                Your wallet number is : {user.wallet.wallet_number}
                                Your alternate wallet number is : {user.wallet.account_number}
                                
                                Thank you for choosing QuickPay!
                                
                                
""",
                                event_type='USER_WALLET_CREATED',


                        )

    send_mail(
        subject="Welcome to Quickpay",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True,
    )

    notification.is_read = True
    notification.save()
    # notification.message

def create_transfer_notification(user, amount):
    wallet = Wallet.objects.create(user=user)
    notification = Notification.objects.create(wallet=user.wallet.wallet_number,
                                               message=f"""***CREDIT ALERT***
                                               {amount} has been credited to ypur wallet,
                                               your new balance is {wallet.balance}
""",
                                               event_type='USER_TRANSFER_NOTIFICATION',)

    send_mail(subject="wallet transfer notification",
              message=notification.message,
              from_email='',
              recipient_list=[user.email],
              fail_silently=True)
    notification.is_read = True
    notification.save()




