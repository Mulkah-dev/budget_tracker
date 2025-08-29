from django import forms
from .models import Transaction, MonthlyBudget
from categories.models import Category

class TransactionForm(forms.ModelForm):
    transaction_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'transaction_date', 'type', 'description']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class MonthlyBudgetForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.none(), empty_label="Select Category")

    class Meta:
        model = MonthlyBudget
        fields = ['month', 'year', 'amount', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)