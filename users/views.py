from django.shortcuts import redirect, render
from shop.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
# Create your views here.

def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartitems = order['get_cart_items']
    context = {
        'products':products,
        'cartitems':cartitems
    }
    return render(request, 'users/home.html',context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
           
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {"form":form})