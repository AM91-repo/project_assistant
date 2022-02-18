from django.contrib.auth import get_user_model
from django.forms import ModelForm, TextInput, CharField, DecimalField, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple

from mainapp.models import *


class FieldsWidgetMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'


class BudgetCreateForm(FieldsWidgetMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(BudgetCreateForm, self).__init__(*args, **kwargs)
        self.fields['users'].widget = CheckboxSelectMultiple()
        self.fields['users'].queryset = User.objects.filter(
            friends=self.request.user)

    # name = CharField()
    # main_budget = BooleanField()
    # description = CharField()
    # amount = DecimalField()
    # users = ModelMultipleChoiceField(
    #     queryset=None,
    #     widget=CheckboxSelectMultiple
    # )

    class Meta:
        model = Budget
        fields = ("name", "description", "amount", "users")


class SourceCreateForm(FieldsWidgetMixin, ModelForm):

    class Meta:
        model = Source
        fields = ("budget", "name_source",
                  "description", "amount_source")


class ExpenseIncomeCreateForm(FieldsWidgetMixin, ModelForm):

    class Meta:
        model = ExpenseIncome
        fields = ("amount", "category", "source", "description", "date_event")


class CategoryCreateForm(FieldsWidgetMixin, ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
