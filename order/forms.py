from datetime import timedelta

from django import forms
from django.forms import DateInput
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User

from .models import Order


# class DateInput(forms.DateInput):
#     input_type = 'date'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('book', 'end_at', 'plated_end_at')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['book'].label_from_instance = lambda book: f'{book.name} ( {book.description[:16]}...)'
        self.fields['book'].empty_label = "Select"
        self.fields['end_at'].widget = forms.DateInput()
        self.fields['plated_end_at'].initial = datetime.now() + timedelta(days=15)
        self.fields['plated_end_at'].widget = forms.HiddenInput()
