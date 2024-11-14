from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import HomeRedirectView
from wallet.views import UserBalanceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeRedirectView.as_view(), name='home'),
    path('api/', include('apps.wallet.urls')),
    path('balance/', UserBalanceView.as_view(), name='balance-view'),
    path('auth/', include('user_auth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)