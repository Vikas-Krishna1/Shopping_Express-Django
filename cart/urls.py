from django.urls import path,include
from . import views

app_name = "cart"

urlpatterns = [
     path("action/", views.cart_action, name="cart_action"),
    path("", views.cart_list, name="cart_list"),
   
]
