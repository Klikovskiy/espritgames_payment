from django.urls import path

from wallet.views import WalletBalanceView, WalletWithdrawView, WalletDepositView, WalletRefundView

urlpatterns = [
    path('balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path('deposit/', WalletDepositView.as_view(), name='wallet-deposit'),
    path('withdraw/', WalletWithdrawView.as_view(), name='wallet-withdraw'),
    path('refund/', WalletRefundView.as_view(), name='wallet-refund'),
]
