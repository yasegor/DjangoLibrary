from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from authentication.utils import send_mail_to_verify
from book.models import Book
from .models import Order
from .forms import OrderForm


@login_required
def all_orders(request):
    if User.objects.filter(id=request.user.id, groups__name='Librarian').exists() or request.user.is_superuser:
        orders = Order.objects.all().order_by('-id').select_related('book')
        page_number = request.GET.get('page', 1)
        paginator = Paginator(orders, 4)
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(number=page_number)
        context = {'title': 'All orders', 'page_range': page_range, 'page_obj': page_obj}
        return render(request, 'order/order_list.html', context)
    else:
        orders = Order.objects.filter(user_id=request.user.id).order_by('-id').select_related('book')
        if not orders.first():
            context = {'title': 'Oops...'}
            return render(request, 'order/no_orders.html', context)
        else:
            page_number = request.GET.get('page', 1)
            paginator = Paginator(orders, 4)
            page_obj = paginator.get_page(page_number)
            page_range = paginator.get_elided_page_range(number=page_number)
            context = {'title': 'My orders', 'page_range': page_range, 'page_obj': page_obj}
            return render(request, 'order/order_user_list.html', context)


@login_required
def create_order(request):
    if request.user.profile.verified:
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.user = request.user
                book = Book.objects.get(id=new_order.book.id)
                book.update(count=book.count - 1)
                new_order.save()
                return redirect('order_list')
            else:
                return render(request, 'order/order_create.html', {'form': form, 'title': 'New order'})
        form = OrderForm()
        return render(request, "order/order_create.html", {"form": form, "title": "New order"})
    else:
        messages.error(request, "Your email hasn't been verified. Check your mail.")
        send_mail_to_verify(request, request.user)


@permission_required('order.change_order', raise_exception=True)
def order_update(request, id):
    order = Order.get_by_id(id)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        context = {'form': form, 'title': 'Order'}
        return render(request, 'order/order_create.html', context)
    else:
        try:
            form = OrderForm(request.POST, instance=order)
            form.save()
            return redirect('order_list')
        except ValueError:
            context = {'form': OrderForm(), 'error': 'Wrong data', 'title': 'Order'}
            return render(request, 'order/order_create.html', context)


@permission_required('order.delete_order', raise_exception=True)
def order_delete(request, id):
    order = Order.get_by_id(id)
    order.delete()
    return redirect('/orders/')
