from unicodedata import category
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
    _total_amount = models.DecimalField(
        'общая сумма', max_digits=15, decimal_places=2, default=0)
    main_budget = models.BooleanField(default=False)
    # sources_finance = models.ManyToManyField(Source)

    def calculation_total_amount(self):
        self._total_amount = self.amount + sum(
            map(lambda x: x.amount_source, self.source_set.all()))
        # list_am = list(map(lambda x: x.amount_source, self.source_set.all()))
        # print(list_am)
        self.save()

    @property
    def get_total_amount(self):
        return self._total_amount

    def __str__(self):
        return self.name


class Source(models.Model):
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE)
    name_source = models.CharField('название', max_length=64)
    description = models.TextField('описание', blank=True)
    amount_source = models.DecimalField(
        'общая сумма', max_digits=15, decimal_places=2, default=0)

    def calculation_amount(self):
        self.amount_source = sum(
            map(lambda x: (float(x.amount) * (-1 if x.expense else 1)),
                self.expenseincome_set.all()))
        # list_am = list(map(lambda x: (float(x.amount) * ((-1) if x.expense else 1)),
        #                    self.expenseincome_set.all()))
        # print(list_am)
        self.save()

    def __str__(self):
        return self.name_source

    # def amount_source(self):
    #     pass


class Category(models.Model):
    name = models.CharField('название', max_length=64)
    description = models.TextField('описание', blank=True)

    def __str__(self):
        return self.name


class ExpenseIncome(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.BooleanField(default=True)
    description = models.TextField('описание', blank=True)
    add_date = models.DateTimeField('время', auto_now_add=True)
    date_event = models.DateField(
        'время события', blank=True, null=True, default=None)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(
        'сумма траты', max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        source = Source.objects.filter(pk=self.source.pk).first()
        budget = Budget.objects.filter(pk=source.budget.pk).first()
        source.calculation_amount()
        budget.calculation_total_amount()


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
