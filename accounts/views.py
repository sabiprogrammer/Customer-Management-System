from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter


# Create your views here.


def home(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': customers, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    items = Product.objects.all()
    return render(request, 'accounts/products.html', {'items': items})


def customer(request, pk):
    client = Customer.objects.get(id=pk)
    orders = client.order_set.all()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {'client': client, 'orders': orders, 'filter': my_filter}
    return render(request, 'accounts/customer.html', context)


def create_order(request, pk):
    FormSetOrder = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    client = Customer.objects.get(id=pk)
    formset = FormSetOrder(queryset=Order.objects.none(), instance=client)
    # form = OrderForm(initial={'customer': client})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = FormSetOrder(request.POST, instance=client)
        if formset.is_valid():
            formset.save()
        return redirect('home')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('home')

    form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    context = {'item': item}
    return render(request, 'accounts/delete.html', context)
