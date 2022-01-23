from django.contrib.auth import get_user_model
from django.forms import ModelForm, HiddenInput

from mainapp.models import Budget


class BudgetCreateForm(ModelForm):
    class Meta:
        model = Budget
        fields = ("name", "description", "amount")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'


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
