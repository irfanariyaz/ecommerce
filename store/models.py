import imp
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE, blank=True)#one user has  one customer
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank = True)
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
            return str(self.id)  #cant return integer so you need to convert into string
    # @property
    # def shipping(self):
	#     shipping = False
    # orderitems = self.orderitem_set.all()
    #     for i in orderitems:
    #         if i.product.digital == False:
    #          shipping = True
    #     return shipping

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital ==False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.get_total for item in orderitems)
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.quantity for item in orderitems)
        return total

    


class OrderItem (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)#product can have multiple orderitem
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)# order can have multiple orderitem
    date_added =  models.DateTimeField(auto_now_add=True) 
    quantity = models.IntegerField(default=0,null=True, blank=True)

    # class Meta:
    #     ordering =['product.name']

    # def __str__(self):
    #     return self.product.name
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

     

class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)#product can have multiple orderitem
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added =  models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.address


  



