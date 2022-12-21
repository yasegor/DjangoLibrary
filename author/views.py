from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from .models import Author
from .forms import AuthorForm


# @cache_page(10 * 60)
def all_authors(request):
    authors = Author.get_all().order_by('name')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(authors, 6)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number)
    context = {'title': 'Authors', 'page_range': page_range, 'page_obj': page_obj}
    return render(request, 'author/author_list.html', context)


@permission_required('author.add_author', raise_exception=True)
@permission_required('author.change_author', raise_exception=True)
def author_form(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = AuthorForm()
        else:
            book = Author.objects.get(pk=id)
            form = AuthorForm(instance=book)
        return render(request, 'author/author_create.html', {'form': form, 'title': 'Author'})
    else:
        if id == 0:
            form = AuthorForm(request.POST)
        else:
            book = Author.objects.get(pk=id)
            form = AuthorForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        return redirect('/authors/')


# @cache_page(15 * 60)
def author_detail(request, id):
    author = get_object_or_404(Author, pk=id)
    books = author.get_books_list()
    context = {'author': author, "books": books, 'title': f'{author.name} {author.surname}'}
    return render(request, 'author/author_detail.html', context)


@permission_required('author.delete_author', raise_exception=True)
def author_delete(request, id):
    author = Author.get_by_id(id)
    author.delete()
    return redirect('/authors/')
