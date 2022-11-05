from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
from django.contrib.auth.models import User


def all_orders(request):
    orders = Order.get_all()
    context = {'orders': orders}
    return render(request, 'order/order_list.html', context)


def create_order(request):
    if request.method == 'GET':
        context = {'form': OrderForm()}
        return render(request, 'order/order_create.html', context)
    else:
        try:
            form = OrderForm(request.POST)
            new_order = form.save()
            new_order.user = request.user
            new_order.save()
            return redirect('order_list')
        except ValueError:
            context = {'form': OrderForm(), 'error': 'Wrong data'}
            return render(request, 'order/order_create.html', context)


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
