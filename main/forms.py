from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']  # Добавим поле для рейтинга

    rating = forms.ChoiceField(
        choices=[(str(i), f'{i} звезда{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect,
        label='Оценка'
    )
