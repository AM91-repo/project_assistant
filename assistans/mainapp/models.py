from django.db import models
from django.contrib.auth import get_user_model
from authapp.models import User


class Budget(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='budgets')
    name = models.CharField('название', max_length=64)
    description = models.TextField('описание', blank=True)
    users = models.ManyToManyField(User)
    amount = models.DecimalField(
        'общая сумма', max_digits=15, decimal_places=2, default=0)
    # sources_finance = models.ManyToManyField(Source)


class Source(models.Model):
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name='source')
    name_source = models.CharField('название', max_length=64)
    description = models.TextField('описание', blank=True)
    amount_source = models.DecimalField(
        'общая сумма', max_digits=15, decimal_places=2, default=0)

    def amount_source(self):
        pass


class Spent(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)
    description = models.TextField('описание', blank=True)
    add_date = models.DateTimeField('время', auto_now_add=True)
    amount_spent = models.DecimalField(
        'сумма траты', max_digits=12, decimal_places=2, default=0)
    # date_spent = models.DateTimeField('время', auto_now_add=True)


class Deposit(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)
    description = models.TextField('описание', blank=True)
    add_date = models.DateTimeField('время', auto_now_add=True)
    amount_deposit = models.DecimalField(
        'сумма добавления', max_digits=12, decimal_places=2, default=0)
    # date_deposit = models.DateTimeField('время', auto_now_add=True)
