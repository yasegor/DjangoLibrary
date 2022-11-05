from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator

from .models import Book
from author.models import Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', "authors", 'description', 'count')
        labels = {
            'name': "Name of book",
            'authors': "Book's Authors",
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['authors'].required = True
        self.fields['name'].required = True
        self.fields['count'].required = True
        self.fields['authors'].queryset = Author.objects.all()
        self.fields['authors'].label_from_instance = lambda obj: "%s %s" % (obj.name, obj.surname)
