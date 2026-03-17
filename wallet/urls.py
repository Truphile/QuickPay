from django.urls import path
from .views import transfer_wallet, fund_wallet

urlpatterns = [
    path("transfer/",transfer_wallet,name="transfer")
    path('deposit/', fund_wallet, name="deposit")
]