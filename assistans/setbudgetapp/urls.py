from django.urls import path

import setbudgetapp.views as setbudgetapp

app_name = 'setbudgetapp'

urlpatterns = [
    path('', setbudgetapp.index, name='index'),
    path('budget/create/', setbudgetapp.BudgetCreate.as_view(),
         name='budget_create'),
    path('budget/update/<int:pk>/', setbudgetapp.BudgetUpdate.as_view(),
         name='budget_update'),
    path('budget/delete/<int:pk>/', setbudgetapp.BudgetDelete.as_view(),
         name='budget_delete'),
    path('budget/basic/<int:pk>/',
         setbudgetapp.set_basic_budget, name='basic_budget'),

    path('budget/<int:pk>/source/', setbudgetapp.source_list,
         name='source_list'),
    #     path('budget/source/<int:pk>/create/', setbudgetapp.SourceCreate.as_view(),
    #          name='source_create'),
    path('budget/<int:budget_pk>/source/create/', setbudgetapp.source_create,
         name='source_create'),
    #     path('budget/<int:budget_pk>/source/update/<int:pk>/', setbudgetapp.source_update,
    #          name='source_update'),
    path('budget/<int:budget_pk>/source/update/<int:pk>/', setbudgetapp.SourceUpdate.as_view(),
         name='source_update'),
    path('budget/source/delete/<int:pk>/', setbudgetapp.SourceDelete.as_view(),
         name='source_delete'),

    path('budget/<int:budget_pk>/source/items/<int:pk>/',
         setbudgetapp.ExpenseIncomeList.as_view(), name='source_details'),
    path('budget/<int:budget_pk>/source/<int:source_pk>/items/createExpense/', setbudgetapp.ExpenseCreate.as_view(),
         name='expense_create'),
    path('budget/<int:budget_pk>/source/<int:source_pk>/items/createIncome/', setbudgetapp.IncomeCreate.as_view(),
         name='income_create'),
    path('budget/<int:budget_pk>/source/item/<int:pk>/update/', setbudgetapp.ExpenseIncomeUpdate.as_view(),
         name='item_update'),
    path('budget/<int:budget_pk>/source/item/<int:pk>/delete/', setbudgetapp.ExpenseIncomeDelete.as_view(),
         name='item_delete'),

    path('category/',
         setbudgetapp.CategoryList.as_view(), name='category'),
    path('category/create/',
         setbudgetapp.CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>/',
         setbudgetapp.CategoryUpdate.as_view(), name='category_update'),
    path('category/delete/<int:pk>/',
         setbudgetapp.CategoryDelete.as_view(), name='category_delete'),
    #     path('budget/source/create/', setbudgetapp.ExpenseIncomeCreate.as_view(),
    #          name='expense_create'),
    #     path('budget/source/create/', setbudgetapp.ExpenseIncomeCreate.as_view(),
    #          name='expense_create'),


]
