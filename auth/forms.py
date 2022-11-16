from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Arnold'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Armstrong'}))
    username = forms.CharField(
        label='Username',
        max_length=30,
        error_messages={'unique': (
            "User with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose your username'})
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
                css_class='form-row'
            ),
            Row(
                Column('password2', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign up')
        )
