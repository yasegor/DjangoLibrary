from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User


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
    email = forms.EmailField(max_length=30,
                             error_messages={
                                 'unique': (
                                     "User with that email already registered."
                                 )
                             },
                             widget=(
                                 forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'})))
    password1 = forms.CharField(label='Password',
                                widget=(forms.PasswordInput(
                                    attrs={'class': 'form-control'})))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-3 mb-3'),
                Column('last_name', css_class='form-group col-md-3 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('username', css_class='form-group col-md-3 mb-3'),
                Column('email', css_class='form-group col-md-3 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-3 mb-0'),
                Column('password2', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign up', css_class='my-3')
        )


class AuthUserForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               max_length=30,
                               error_messages={'unique': (
                                   "User with that username already exists.")},
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(label='Password',
                               widget=(forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter your password'})))

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-3 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign in', css_class='my-3')
        )
