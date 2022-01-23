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

    budgets = request.user.budgets.all()
    if not budgets:
        budget_exists = False

    context = {
        'budget_exists': budget_exists,
        'budgets': budgets,
        'page_title': 'главная',
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
