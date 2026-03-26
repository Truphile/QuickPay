from django.urls import path
from .views import transfer_wallet, fund_wallet, funded_wallet, dashboard
from wallet.services.fund_wallet import paystack_callback

urlpatterns = [
    path("transfer/",transfer_wallet,name="transfer"),
    path('deposit/', fund_wallet, name="deposit"),
    path('callback/', paystack_callback, name="paystack_callback"),
    path('fund/', funded_wallet, name="fund_wallet"),
    path('dashboard/', dashboard, name="dashboard"),
]