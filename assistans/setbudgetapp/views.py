from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth import get_user_model


from setbudgetapp.forms import BudgetCreateForm, SourceCreateForm, ExpenseIncomeCreateForm, CategoryCreateForm
from mainapp.models import Budget, Source, ExpenseIncome, Category


@login_required
def index(request):
    all_budgets = Budget.objects.filter(
        Q(user_created=request.user) | Q(users=request.user)).all()
    context = {
        'page_title': 'настройки',
        'all_budgets': all_budgets,
    }
    return render(request, 'setbudgetapp/index.html', context)


@login_required
def set_basic_budget(request, pk):
    user = get_user_model().objects.get(id=request.user.id)
    user.basic_budget = Budget.objects.get(id=pk)
    user.save()
    return HttpResponseRedirect(reverse('set:index'))


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
        obj.user_created = self.request.user
        return super(BudgetCreate, self).form_valid(form)

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(BudgetCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BudgetCreate, self).get_context_data(**kwargs)
        context['update'] = False
        return context


class BudgetUpdate(UserIsAuthMixin, PageTitleMixin, UpdateView):
    model = Budget
    form_class = BudgetCreateForm
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/редактирование'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""
        kwargs = super(BudgetUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BudgetUpdate, self).get_context_data(**kwargs)
        context['update'] = True
        return context


class BudgetDelete(UserIsAuthMixin, PageTitleMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('set:index')
    page_title = 'управление/бюджет/удаление'


class SourceDelete(UserIsAuthMixin, PageTitleMixin, DeleteView):
    model = Source
    # success_url = reverse_lazy('set:source_list')
    page_title = 'управление/бюджет/источник/удаление'

    def get_success_url(self):
        return reverse('set:source_list', kwargs={'pk': self.object.budget.pk})


class SourceUpdate(UserIsAuthMixin, PageTitleMixin, UpdateView):
    model = Source
    form_class = SourceCreateForm
    template_name = 'mainapp/source_form.html'
    # success_url = reverse_lazy(self.request.META.get('HTTP_REFERER'))
    page_title = 'управление/бюджет/источник/редактирование'

    def get_success_url(self):
        return reverse('set:source_list', kwargs={'pk': self.object.budget.pk})

    def get_context_data(self, **kwargs):
        context = super(SourceUpdate, self).get_context_data(**kwargs)
        context['budget_pk'] = self.request.resolver_match.kwargs['budget_pk']
        return context


@login_required
def source_list(request, pk):
    budget_pk = pk
    budget = get_object_or_404(Budget, pk=budget_pk)
    object_list = budget.source_set.all()
    context = {
        'page_title': 'управление/бюджет/источники',
        'budget_pk': budget_pk,
        'object_list': object_list,
    }
    return render(request, 'mainapp/source_list.html', context)


@login_required
def source_create(request, budget_pk):
    budget = get_object_or_404(Budget, pk=budget_pk)
    budget_pk = budget.pk
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
        'budget_pk': budget_pk,
    }
    return render(request, 'mainapp/source_form.html', context)


class ExpenseIncomeList(UserIsAuthMixin, PageTitleMixin, ListView):
    model = ExpenseIncome
    # template_name = 'xxxx_app/xxxx.html'
    page_title = 'управление/бюджет/источник/детали'
    # queryset = ExpenseIncome.objects.filter(source=self.object.source.pk)

    def get_queryset(self):
        return ExpenseIncome.objects.filter(source=self.request.resolver_match.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ExpenseIncomeList, self).get_context_data(**kwargs)
        context['budget_pk'] = self.request.resolver_match.kwargs['budget_pk']
        context['source_pk'] = self.request.resolver_match.kwargs['pk']
        # print(context)
        return context


class ExpenseIncomeCreateMixin:
    model = ExpenseIncome
    form_class = ExpenseIncomeCreateForm
    http_referer = ''

    def get_success_url(self):
        # print(self.request.META.get('HTTP_REFERER'))
        print(self.request.POST.get('next'))

        if '/set' in self.request.POST.get('next'):
            return reverse('set:source_details',
                           kwargs={'pk': self.object.source.pk,
                                   'budget_pk': self.object.source.budget.pk})
        else:
            return reverse('base:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budget_pk'] = self.request.resolver_match.kwargs['budget_pk']
        context['source_pk'] = self.request.resolver_match.kwargs['source_pk']
        context['url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_initial(self):
        # self.http_referer = self.request.POST.get('next')
        initial = super().get_initial()
        initial = initial.copy()
        initial['source'] = self.request.resolver_match.kwargs['source_pk']
        return initial


class IncomeCreate(UserIsAuthMixin, PageTitleMixin, ExpenseIncomeCreateMixin, CreateView):
    model = ExpenseIncome
    form_class = ExpenseIncomeCreateForm
    template_name = 'mainapp/income_form.html'
    page_title = 'управление/бюджет/источник/детали/создание'

    def form_valid(self, form):
        self.http_referer = self.request.POST.get('next')
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.expense = False
        return super(IncomeCreate, self).form_valid(form)


class ExpenseCreate(UserIsAuthMixin, PageTitleMixin, ExpenseIncomeCreateMixin, CreateView):
    model = ExpenseIncome
    form_class = ExpenseIncomeCreateForm
    template_name = 'mainapp/expense_form.html'
    page_title = 'управление/бюджет/источник/детали/создание'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.expense = True
        return super(ExpenseCreate, self).form_valid(form)


class ExpenseIncomeUpdate(UserIsAuthMixin, PageTitleMixin, UpdateView):
    model = ExpenseIncome
    form_class = ExpenseIncomeCreateForm
    template_name = 'mainapp/expense_form.html'
    # success_url = reverse_lazy(self.request.META.get('HTTP_REFERER'))
    page_title = 'управление/бюджет/источник/редактирование'

    def get_success_url(self):
        return reverse('set:source_details',
                       kwargs={'pk': self.object.source.pk,
                               'budget_pk': self.object.source.budget.pk})

    def get_context_data(self, **kwargs):
        context = super(ExpenseIncomeUpdate, self).get_context_data(**kwargs)
        context['budget_pk'] = self.request.resolver_match.kwargs['budget_pk']
        # context['source_pk'] = self.request.resolver_match.kwargs['source_pk']
        return context


class ExpenseIncomeDelete(UserIsAuthMixin, PageTitleMixin, DeleteView):
    model = ExpenseIncome
    template_name = 'mainapp/expenseincome_delete.html'
    page_title = 'управление/бюджет/источник/детали/удаление'

    def get_success_url(self):
        return reverse('set:source_details',
                       kwargs={'pk': self.object.source.pk,
                               'budget_pk': self.request.resolver_match.kwargs['budget_pk']})

    def get_context_data(self, **kwargs):
        context = super(ExpenseIncomeList, self).get_context_data(**kwargs)
        context['budget_pk'] = self.request.resolver_match.kwargs['budget_pk']
        context['source_pk'] = self.request.resolver_match.kwargs['pk']
        return context


class CategoryList(UserIsAuthMixin, PageTitleMixin, ListView):
    model = Category
    page_title = 'управление/категории'


class CategoryCreate(UserIsAuthMixin, PageTitleMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('set:category')
    page_title = 'управление/категории/создание'


class CategoryUpdate(UserIsAuthMixin, PageTitleMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('set:category')
    page_title = 'управление/категории/редактирование'


class CategoryDelete(UserIsAuthMixin, PageTitleMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('set:category')
    page_title = 'управление/категории/удаление'
