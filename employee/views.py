from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from orders.models import Order
from items.models import Item
from . import views

def is_employee(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.user_type.lower() == "employee"
    )

@user_passes_test(is_employee)
def dashboard(request):
    return render(request, "employee/dashboard.html")

@user_passes_test(is_employee)
def orders_list(request):
    orders = Order.objects.filter(status="pending").order_by("created_at")
    return render(request, "employee/orders.html", {"orders": orders})

@user_passes_test(is_employee)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "employee/order_details.html", {"order": order})

@user_passes_test(is_employee)
def inventory(request):
    items = Item.objects.all().order_by("name")
    return render(request, "employee/inventory.html", {"items": items})
