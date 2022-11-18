from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Book
from .forms import BookForm


def all_books(request):
    books = Book.get_all()
    context = {'books': books}
    return render(request, 'book/book_list.html', context)


def book_form(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = BookForm()
        else:
            book = Book.objects.get(pk=id)
            form = BookForm(instance=book)
        return render(request, 'book/book_create.html', {'form': form})
    else:
        if id == 0:
            form = BookForm(request.POST)
        else:
            book = Book.objects.get(pk=id)
            form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()

        return redirect('/books/')


def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    context = {'book': book}
    return render(request, 'book/book_detail.html', context)


def book_delete(request, id):
    book = Book.get_by_id(id)
    book.delete()
    return redirect('/books/')
