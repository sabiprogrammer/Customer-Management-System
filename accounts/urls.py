from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('create_order/<pk>', views.create_order, name='create_order'),
    path('update_order/<pk>', views.update_order, name='update_order'),
    path('delete_order/<pk>', views.delete_order, name='delete_order'),
    path('customer/<pk>', views.customer, name='customer'),
]
