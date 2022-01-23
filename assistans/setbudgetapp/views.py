from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView


from setbudgetapp.forms import BudgetCreateForm
from mainapp.models import Budget


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda user: user.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title_key = 'page_title'
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.page_title_key] = self.page_title
        return context


class BudgetCreate(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = Budget
    form_class = BudgetCreateForm
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/создание'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(BudgetCreate, self).form_valid(form)


class BudgetUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = Budget
    form_class = BudgetCreateForm
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/редактирование'


class BudgetDelete(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/удаление'


@login_required
def index(request):
    all_budgets = request.user.budgets.all()
    context = {
        'page_title': 'настройки',
        'all_budgets': all_budgets,
    }
    return render(request, 'setbudgetapp/index.html', context)
