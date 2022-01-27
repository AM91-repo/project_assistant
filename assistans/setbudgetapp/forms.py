from django.contrib.auth import get_user_model
from django.forms import ModelForm, HiddenInput

from mainapp.models import *


class FieldsWidgetMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'


class BudgetCreateForm(FieldsWidgetMixin, ModelForm):
    class Meta:
        model = Budget
        fields = ("name", "description", "amount")


class SourceCreateForm(FieldsWidgetMixin, ModelForm):
    class Meta:
        model = Source
        fields = ("budget", "name_source", "description", "amount_source")


class ExpenseIncomeCreateForm(FieldsWidgetMixin, ModelForm):
    class Meta:
        model = ExpenseIncome
        fields = ("amount", "category", "source", "description", "date_event")


class CategoryCreateForm(FieldsWidgetMixin, ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


# class AdminProductUpdateForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             if field_name == 'category':
#                 field.widget = HiddenInput()
