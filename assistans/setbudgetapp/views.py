from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView


from setbudgetapp.forms import BudgetCreateForm, SourceCreateForm, ExpenseIncomeCreateForm, CategoryCreateForm
from mainapp.models import Budget, Source, ExpenseIncome, Category


class UserIsAuthMixin:
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


class BudgetCreate(UserIsAuthMixin, PageTitleMixin, CreateView):
    model = Budget
    form_class = BudgetCreateForm
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/создание'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(BudgetCreate, self).form_valid(form)


class BudgetUpdate(UserIsAuthMixin, PageTitleMixin, UpdateView):
    model = Budget
    form_class = BudgetCreateForm
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/редактирование'


class BudgetDelete(UserIsAuthMixin, PageTitleMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/удаление'


# class SourceList(ListView):
#     model = Source
#     # template_name = 'xxxx_app/xxxx.html'
#     page_title = 'управление/бюджет/источник'

#     def get_queryset(self):
#         return Source.objects.filter(budget=self.request.resolver_match.kwargs['pk'])


class SourceCreate(UserIsAuthMixin, PageTitleMixin, CreateView):
    model = Source
    form_class = SourceCreateForm
    success_url = reverse_lazy('set:source_list')
    page_title = 'управление/бюджет/источник/создание'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(SourceCreate, self).form_valid(form)


class SourceUpdate(UserIsAuthMixin, PageTitleMixin, UpdateView):
    model = Source
    form_class = SourceCreateForm
    success_url = reverse_lazy('set:source_list')
    page_title = 'управление/бюджет/источник/редактирование'


class SourceDelete(UserIsAuthMixin, PageTitleMixin, DeleteView):
    model = Source
    success_url = reverse_lazy('set:source_list')
    page_title = 'управление/бюджет/источник/удаление'


@login_required
def source_list(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    object_list = budget.source_set.all()
    context = {
        'page_title': 'управление/бюджет/источники',
        'pk': pk,
        'object_list': object_list,
    }
    return render(request, 'mainapp/source_list.html', context)


def source_create(request, budget_pk):
    budget = get_object_or_404(Budget, pk=budget_pk)
    if request.method == 'POST':
        form = SourceCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'set:source_list',
                kwargs={'pk': budget.pk}
            ))
    else:
        form = SourceCreateForm(
            initial={
                'budget': budget,
            }
        )

    context = {
        'page_title': 'управление/бюджет/источник/создание',
        'form': form,
        'budget': budget,
    }
    return render(request, 'mainapp/source_form.html', context)


@login_required
def index(request):
    all_budgets = request.user.budgets.all()
    context = {
        'page_title': 'настройки',
        'all_budgets': all_budgets,
    }
    return render(request, 'setbudgetapp/index.html', context)
