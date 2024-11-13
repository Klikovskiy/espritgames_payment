from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """ Управление балансом пользователей. """

    list_display = ('user', 'balance', 'last_updated')
    readonly_fields = ('last_updated',)
