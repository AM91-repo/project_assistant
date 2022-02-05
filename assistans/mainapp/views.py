from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mainapp.models import Budget


# from django.contrib import auth
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib.auth import get_user_model


@login_required
def index(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('auth:login'))
    # print(request.user)
    budget_exists = True

    budget = request.user.budgets.filter(main_budget=True).first()
    if not budget:
        budget_exists = False

    total_amount = budget.get_total_amount

    context = {
        'budget_exists': budget_exists,
        'budgets': budget,
        'page_title': 'главная',
        'total_amount': total_amount,
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
