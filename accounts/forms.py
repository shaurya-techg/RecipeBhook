from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


INPUT_CLASS = (
    "w-full rounded-xl border border-stone-300 bg-stone-50 "
    "px-4 py-3 text-stone-900 outline-none transition "
    "placeholder:text-stone-400 "
    "focus:border-orange-400 focus:bg-white "
    "focus:ring-4 focus:ring-orange-100"
)




class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "Enter your email address",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "Choose a username",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {
                "class": INPUT_CLASS,
                "placeholder": "Create a password",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": INPUT_CLASS,
                "placeholder": "Confirm your password",
            }
        )