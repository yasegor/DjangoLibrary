from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from .models import Book
from .forms import BookForm


# @cache_page(10 * 60)
def all_books(request):
    books = Book.get_all().order_by('-id')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(books, 4)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number)
    context = {'title': 'Books', 'page_range': page_range, 'page_obj': page_obj}
    return render(request, 'book/book_list.html', context)


@permission_required('book.add_book', raise_exception=True)
@permission_required('book.change_book', raise_exception=True)
def book_form(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = BookForm()
        else:
            book = Book.objects.get(pk=id)
            form = BookForm(instance=book)
        return render(request, 'book/book_create.html', {'form': form, 'title': 'Book'})
    else:
        if id == 0:
            form = BookForm(request.POST)
        else:
            book = Book.objects.get(pk=id)
            form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()

        return redirect('/books/')


# @cache_page(15 * 60)
def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    context = {'book': book, 'title': book.name}
    return render(request, 'book/book_detail.html', context)


@permission_required('book.delete_book', raise_exception=True)
def book_delete(request, id):
    book = Book.get_by_id(id)
    book.delete()
    return redirect('/books/')
