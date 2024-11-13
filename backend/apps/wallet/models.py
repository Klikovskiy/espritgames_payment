
from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    """Кошелек пользователя."""

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(verbose_name='Баланс', max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    def deposit(self, amount):
        """Пополнение баланса"""
        if amount <= 0:
            raise ValueError('Сумма пополнения должна быть положительной')
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Списание средств"""
        if amount <= 0:
            raise ValueError('Сумма для снятия должна быть положительной')
        if amount > self.balance:
            raise ValueError('Недостаточно средств на счете')
        self.balance -= amount
        self.save()

    def refund(self, amount):
        """Возврат средств"""
        if amount <= 0:
            raise ValueError('Сумма возврата должна быть положительной')
        self.deposit(amount)

    def __str__(self):
        return f'Кошелек {self.user.username} с балансом {self.balance}'

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'
