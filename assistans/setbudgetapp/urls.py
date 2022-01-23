from django.urls import path

import setbudgetapp.views as setbudgetapp

app_name = 'setbudgetapp'

urlpatterns = [
    path('', setbudgetapp.index, name='index'),
    path('budget/create/', setbudgetapp.BudgetCreate.as_view(),
         name='budget_create'),
    path('budget/update/<int:pk>/', setbudgetapp.BudgetUpdate.as_view(),
         name='budget_update'),
    path('category/delete/<int:pk>/', setbudgetapp.BudgetDelete.as_view(),
         name='budget_delete'),

    #     path('user/update/<int:user_pk>/', setbudgetapp.ShopUserAdminUpdate.as_view(),
    #          name='user_update'),

    #     path('user/delete/<int:user_pk>/', setbudgetapp.user_delete, name='user_delete'),

    #     path('category/<int:pk>/products/',
    #          setbudgetapp.category_products, name='category_products'),
    #     path('category/<int:category_pk>/product/create/', setbudgetapp.category_product_create,
    #          name='category_product_create'),

    #     path('product/<int:pk>/', setbudgetapp.ProductDetail.as_view(), name='product_view'),

    #     path('product/update/<int:pk>/', setbudgetapp.ProductUpdate.as_view(),
    #          name='product_update'),
    #     path('product/delete/<int:pk>/', setbudgetapp.ProductDelete.as_view(),
    #          name='product_delete'),


]
