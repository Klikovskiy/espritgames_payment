from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from user_auth.forms import LoginForm


class CustomLoginView(LoginView):
    """ Страница для входа пользователя. """

    template_name = 'auth/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('balance-view')