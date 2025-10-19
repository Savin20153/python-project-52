from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")
        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
            "username": _("Имя пользователя"),
            "password1": _("Пароль"),
            "password2": _("Подтверждение пароля"),
        }


class UserUpdateForm(forms.ModelForm):
    # Дополнительные поля для смены пароля (необязательные)
    password = forms.CharField(
        label=_("Пароль"), widget=forms.PasswordInput, required=False
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"), widget=forms.PasswordInput, required=False
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
        labels = {
            "first_name": _("Имя"),
            "last_name": _("Фамилия"),
            "username": _("Имя пользователя"),
            "email": _("Email"),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password2")
        if p1 or p2:
            if not p1 or not p2:
                raise forms.ValidationError(_("Необходимо ввести оба поля пароля"))
            if p1 != p2:
                raise forms.ValidationError(_("Пароли не совпадают"))
        return cleaned
