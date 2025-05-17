from django import forms
from .models import Category, Expense


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'})
        }
        labels = {
            'name': 'Название категории',
            'color': 'Цвет категории',
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'comment', 'photo']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Сумма расхода должна быть положительной.')
        return amount

class ExpenseEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'comment', 'photo']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Сумма расхода должна быть положительной.')
        return amount
