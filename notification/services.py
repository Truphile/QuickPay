import notification
from notification.models import Notification
from django.core.mail import send_mail


def create_notification(user):
    Notification.objects.create(user=user,
                                message=f"""
                                Hi {user.first_name} Welcome to Quickpay!
                                Your wallet number is : {user.wallet_number}
                                Your alternate wallet number is : {user.wallet.account_number}
""")

    send_mail(
        subject="Quickpay Notification",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True,
    )

    notification.is_read = True
    notification.save()