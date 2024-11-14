from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from wallet.views import WalletBalanceView, WalletWithdrawView, WalletDepositView, WalletRefundView

schema_view = get_schema_view(
    openapi.Info(
        title='API для кошелька',
        default_version='v1',
        description='API для работы с кошельком пользователя',
        contact=openapi.Contact(email='contact@espritgames.ru'),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path('deposit/', WalletDepositView.as_view(), name='wallet-deposit'),
    path('withdraw/', WalletWithdrawView.as_view(), name='wallet-withdraw'),
    path('refund/', WalletRefundView.as_view(), name='wallet-refund'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
