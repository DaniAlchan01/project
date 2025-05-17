from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import re

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Логин"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Подтвердите пароль"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        # Проверка сложности пароля
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать хотя бы 8 символов.")
        if not re.search(r"\d", password):  # Должен быть хотя бы один символ
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
        return password

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Логин"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Пароль"})

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["avatar", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise ValidationError("Этот email уже используется другим пользователем.")
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            # Можно добавить дополнительные проверки для изображения (размер, формат и т.д.)
            if avatar.size > 5 * 1024 * 1024:  # Максимальный размер 5 МБ
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")
        return avatar

class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({"class": "form-control", "placeholder": "Новый пароль"})
        self.fields["new_password2"].widget.attrs.update({"class": "form-control", "placeholder": "Подтвердите пароль"})

    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")
        # Проверка сложности нового пароля
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать хотя бы 8 символов.")
        if not re.search(r"\d", password):  # Должен быть хотя бы один символ
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
        return password

class PasswordResetByLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите ваш логин"})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = CustomUser.objects.filter(username=username).first()
        if not user:
            raise ValidationError("Пользователь с таким логином не найден.")
        return username

class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username"]
        labels = {"username": "Новый логин"}
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите новый логин"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Этот логин уже занят.")
        if " " in username:  # Запрещаем пробелы в логине
            raise ValidationError("Логин не может содержать пробелы.")
        return username

class PaymentCardForm(forms.Form):
    card_number = forms.CharField(max_length=16, min_length=16, label="Номер карты",
                                  widget=forms.TextInput(attrs={'placeholder': 'Номер карты', 'maxlength': 16}))
    cardholder_name = forms.CharField(max_length=100, label="Имя владельца карты",
                                      widget=forms.TextInput(attrs={'placeholder': 'Имя владельца карты'}))
    expiry_date = forms.CharField(max_length=5, min_length=5, label="Срок действия (мм/гг)",
                                  widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, min_length=3, label="CVV",
                          widget=forms.TextInput(attrs={'placeholder': 'CVV'}))
