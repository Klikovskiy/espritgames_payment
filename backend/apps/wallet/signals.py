from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wallet


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    """ Автоматическое создание кошелька при создании пользователя. """
    if created:
        Wallet.objects.create(user=instance)