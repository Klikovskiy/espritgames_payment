from django.urls import reverse
from django.views.generic import RedirectView


class HomeRedirectView(RedirectView):
    """
    Перенаправляет на страницу баланса, если пользователь авторизован.
    Если не авторизован, перенаправляет на страницу входа.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('balance-view')
        return reverse('user_auth:login')
