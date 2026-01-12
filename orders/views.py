from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from cart.models import CartItem
from .models import Order, OrderItem

@login_required
@transaction.atomic
def checkout(request):
    cart_items = CartItem.objects.select_related("item").filter(user=request.user)

    if not cart_items.exists():
        return redirect("items:items_list")

    total = sum(ci.item.price * ci.quantity for ci in cart_items)

    # Create order
    order = Order.objects.create(
        user=request.user,
        total=total,
    )

    # Create order items + reduce stock
    for ci in cart_items:
        OrderItem.objects.create(
            order=order,
            item=ci.item,
            price=ci.item.price,
            quantity=ci.quantity,
        )

        ci.item.stock -= ci.quantity
        ci.item.save()

    # Clear cart
    cart_items.delete()

    return redirect("orders:detail", order_id=order.id)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_detail.html",
        {"order": order}
    )
