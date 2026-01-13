from django.urls import path
from . import views
from .  import views

app_name = "employee"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("orders/", views.orders_list, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order-detail"),
    path("inventory/", views.inventory, name="inventory"),
]
