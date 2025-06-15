from django import forms
from .models import Review
from SourceProg.models import SpendingLimit

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']  # Добавим поле для рейтинга

    rating = forms.ChoiceField(
        choices=[(str(i), f'{i} звезда{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect,
        label='Оценка'
    )

class LimitForm(forms.ModelForm):
    class Meta:
        model = SpendingLimit
        fields = ['monthly_limit']
        labels = {'monthly_limit': 'Текущий лимит (₸)'}
        widgets = {
            'monthly_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите лимит...'
            })
        }