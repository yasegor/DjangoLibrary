from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import timedelta
from django import forms
from django.forms import DateInput
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User

from .models import Order
from book.models import Book


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('book', 'end_at', 'plated_end_at')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['book'].label_from_instance = lambda book: f'{book.name} ( {book.description[:20]}...)'
        self.fields['book'].empty_label = "Select the book"
        self.fields['end_at'].widget = DatePickerInput(options={
            "format": "DD/MM/YYYY",
            "showTodayButton": True,
            "showClose": True,
            "showClear": True,
            "allowInputToggle": True,
        })
        self.fields['plated_end_at'].initial = datetime.now() + timedelta(days=15)
        self.fields['plated_end_at'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        book_id = cleaned_data.get('book').id
        end_at_date = cleaned_data.get('end_at')
        books_count = Book.get_by_id(book_id).count
        if books_count == 0:
            raise forms.ValidationError("There are no more books like this in the library!")
        if not end_at_date:
            raise forms.ValidationError("End date hasn't been set!")

        return self.cleaned_data
