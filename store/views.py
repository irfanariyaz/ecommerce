
from asyncio import ProactorEventLoop
from itertools import product
from urllib import response
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder

# Create your views here.
def store(request):
    products = Product.objects.all()
    data = cartData(request)
    cartTotal = data['cartTotal']
           
    context = {'products': products,'cartTotal':cartTotal}
    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)
    cartTotal = data['cartTotal']
    items = data['items']
    order = data['order']

                
    context = {'items':items,'order':order,'cartTotal':cartTotal}
    return render(request,'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartTotal = data['cartTotal']
    items = data['items']
    order = data['order']

               
    context = {'items':items,'order':order,'cartTotal':cartTotal }
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('ProductId',productId)
    print('Action',action) 
    
    customer = request.user.customer
    product = Product.objects.get( id= productId)
    order,created  = Order.objects.get_or_create(customer = customer,complete = False)
    orderitems ,created = OrderItem.objects.get_or_create(order = order,product = product)
    print('orderitems',orderitems)
    if action == 'add':
        orderitems.quantity = orderitems.quantity + 1
    elif action == 'remove':
        orderitems.quantity = orderitems.quantity - 1
    orderitems.save()

    if orderitems.quantity <= 0:
        orderitems.delete()

    return JsonResponse('item was added',safe=False)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def proccessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('data from processed order',data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created  = Order.objects.get_or_create(customer = customer,complete = False)
        
    else:
        customer,order = guestOrder(request,data)

        
    total = data['form']['total']
    order.transaction_id = transaction_id

    if float(total) == float(order.get_cart_total):
        print('order was complete')
        order.complete = True
    order.save()

    if order.shipping == True:
           
            ShippingAdress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
                
            )

    return JsonResponse('Payment complete',safe =False)