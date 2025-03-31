from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from .models import CustomUser
from django.core.exceptions import ValidationError

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

class ChangePasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({"class": "form-control", "placeholder": "Новый пароль"})
        self.fields["new_password2"].widget.attrs.update({"class": "form-control", "placeholder": "Подтвердите пароль"})

class PasswordResetByLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите ваш логин"})
    )

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
        return username
