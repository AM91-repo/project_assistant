from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auth:login'))

    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)
