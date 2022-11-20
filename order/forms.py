from datetime import timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Submit
from django import forms
from django.forms import DateInput
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User

from .models import Order
from book.models import Book


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('book', 'end_at', 'plated_end_at')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['book'].label_from_instance = lambda book: f'{book.name} ( {book.description[:20]}...)'
        self.fields['book'].empty_label = "Select the book"
        self.fields['end_at'].widget = DatePickerInput()
        self.fields['plated_end_at'].initial = datetime.now() + timedelta(days=15)
        self.fields['plated_end_at'].widget = forms.HiddenInput()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column('book', css_class='form-group col-md-3 mb-3'),
            Column('end_at', css_class='form-group col-md-3 mb-3'),
            Column('plated_end_at', css_class='form-group col-md-3 mb-3'),
            Submit('submit', 'Add order', css_class='my-3')
        )

    def clean(self):
        cleaned_data = super().clean()
        book_id = cleaned_data.get('book').id
        end_at_date = cleaned_data.get('end_at')
        books_count = Book.get_by_id(book_id).count
        if books_count == 0:
            raise forms.ValidationError("There are no more books like this in the library!")
        if not end_at_date:
            raise forms.ValidationError("End date not set!")

        return self.cleaned_data
