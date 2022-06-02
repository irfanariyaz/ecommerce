import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])# converts to a dictionary
    except:
        cart = {}
    print('cart-cookie',cart)
    items = []
    order= {'get_cart_total': 0,'get_cart_items':0,'shipping': False}
    cartTotal = order['get_cart_items']

    for i in cart:
        try:

            cartTotal += cart[i]['quantity']

            product = Product.objects.get(id = i)
            total =product.price * cart[i]['quantity']
            print('total of each product',total)
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartTotal':cartTotal,'items':items,'order':order}

def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()#here all model names are lowercase.parent is order and child is orderitems
        cartTotal = order.get_cart_items   
    else:
        cookieData = cookieCart(request)
        cartTotal = cookieData['cartTotal']
        items = cookieData['items']
        order = cookieData['order']
    return {'items':items,'order':order,'cartTotal':cartTotal}

def guestOrder(request,data):
    print("useer is not logged in ")
    print('COoKIES',request.COOKIES['cart'])
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)#this is a dictionary from the cart cookies
    items = cookieData['items']
    
    customer, created = Customer.objects.get_or_create(
        email = email
        )
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer = customer,
        complete = False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )

    return customer,order