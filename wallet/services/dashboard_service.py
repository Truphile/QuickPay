from wallet.models import Transaction


def get_dashboard_data(user):
    wallet = user.wallet
    transactions = Transaction.objects.filter(sender=wallet).order_by('-created_at')[:5]
    return {
        "message": f"hi,{user.first_name}",
        "wallet": wallet.wallet_number,
        "transactions": transactions,
        "balance": wallet.balance,
        "status": wallet.status,
        "currency": wallet.currency,
    }