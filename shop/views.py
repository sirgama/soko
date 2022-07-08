import json
from django.shortcuts import render
from .models import *
from users.models import Customer
from django.http import JsonResponse


# Create your views here.
def store(request):
    
    
    context = {
        
    }
    return render(request, 'shop/store.html', context)



def cart(request):
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
        'items':items,
        'order':order,
        'cartitems':cartitems
    }
    return render(request, 'shop/cart.html', context)

def checkout(request):
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
        'items':items,
        'order':order,
        'cartitems':cartitems,
    }
    return render(request, 'shop/checkout.html', context)
# from django.views.decorators.csrf import csrf_protect

# @csrf_protect
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('productId:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item added', safe=False)

def processOrder(request):
    print('Data', request.body)
    return JsonResponse('Payment complete', safe=False)