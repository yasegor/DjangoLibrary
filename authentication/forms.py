from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Robert'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paulson'}))
    username = forms.CharField(
        label='Username',
        max_length=30,
        error_messages={'unique': (
            "User with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(required=True, max_length=40,
                             widget=(
                                 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'})))
    password1 = forms.CharField(label='Password',
                                widget=(forms.PasswordInput(
                                    attrs={'class': 'form-control'})))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'User with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)


class AuthUserForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(label='Password', error_messages={
        'unique': (
            "This password is incorrect."
        )
    },
                               widget=(forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter your password'})))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), label=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        user = User.objects.get(username=username)
        if not user.profile.verified:
            raise ValidationError("Your email isn't verified. Check your email inbox and try again.")
        return self.cleaned_data
