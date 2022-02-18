from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from mainapp.models import Budget, ExpenseIncome


@login_required
def index(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('auth:login'))
    # print(request.user)
    page_num = request.GET.get('page')
    budget_exists = True

    budget = request.user.basic_budget
    if not budget:
        budget_exists = False
        source = False
        total_amount = 0
        expense_income = False
    else:
        total_amount = budget.get_total_amount
        source = budget.source_set.filter(budget=budget.pk).first()

        source_name = list(
            name.id for name in budget.source_set.filter(budget=budget.pk))
        # expense_income = request.user.expenseincome_set.filter(
        #     source__id__in=source_name).order_by('-add_date')
        expense_income = ExpenseIncome.objects.filter(
            source__id__in=source_name).order_by('-add_date')

        expense_income_paginator = Paginator(expense_income, 10)
        try:
            expense_income = expense_income_paginator.get_page(page_num)
        except PageNotAnInteger:
            expense_income = expense_income_paginator.get_page(1)
        except EmptyPage:
            expense_income = expense_income_paginator.get_page(
                expense_income_paginator.num_pages)

    context = {
        'budget_exists': budget_exists,
        'budget': budget,
        'page_title': 'главная',
        'total_amount': total_amount,
        'source': source,
        'expense_income': expense_income
    }
    return render(request, 'mainapp/index.html', context)


def description(request):
    contacts = [
        {'city': 'Санкт-петербург',
         'phone': '+7-123-456-7890',
         'email': 'infoS@basketballshop',
         'address': 'Эрмитаж', },
    ]
    context = {
        'page_title': 'контакты',
        'contacts': contacts,
    }
    return render(request, 'mainapp/contact.html', context)
