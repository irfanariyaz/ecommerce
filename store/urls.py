from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update-item/',views.updateItem,name='update-item'),
    path('process-order/',views.proccessOrder,name='process-order'),
    path('product/<int:pk>/',views.productDetail,name='product_details'),
]