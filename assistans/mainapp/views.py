from django.shortcuts import render


def index(request):
    print(request.headers)
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)
