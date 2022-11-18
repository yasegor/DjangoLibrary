from django.shortcuts import render, get_object_or_404, redirect

from book.models import Book
from .models import Order
from .forms import OrderForm
from django.contrib.auth.models import User


def all_orders(request):
    orders = Order.objects.all().order_by('-id')
    context = {'orders': orders}
    return render(request, 'order/order_list.html', context)


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            new_order.user = request.user
            book = Book.objects.get(id=new_order.book.id)
            book.update(count=book.count - 1)
            new_order.save()
            return redirect('order_list')
        else:
            return render(request, 'order/order_create.html', {'form': form, 'title': 'New order'})
    form = OrderForm()
    return render(request, "order/order_create.html", {"form": form, "title": "New order"})


def order_detail(request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == 'GET':
        context = {'order': order}
        return render(request, 'order/order_detail.html', context)
    else:
        order.delete()
        return redirect('order_list')


def order_update(request, id):
    order = Order.get_by_id(id)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        context = {'form': form}
        return render(request, 'order/order_create.html', context)
    else:
        try:
            form = OrderForm(request.POST, instance=order)
            form.save()
            return redirect('order_list')
        except ValueError:
            context = {'form': OrderForm(), 'error': 'Wrong data'}
            return render(request, 'order/order_create.html', context)
