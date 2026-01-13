from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from items.models import Item
from .models import CartItem

@login_required
def cart_action(request):
    action = request.POST.get("action")
    selected_items = request.POST.getlist("selected_items")

    if action == "clear":
        CartItem.objects.filter(user=request.user).delete()
        return redirect("items:items_list")

    if not selected_items:
        return redirect("items:items_list")

    if action == "remove":
        CartItem.objects.filter(
            user=request.user,
            item_id__in=selected_items
        ).delete()
        return redirect("items:items_list")

    if action == "add":
        for item_id in selected_items:
            quantity = int(request.POST.get(f"quantity_{item_id}", 0))
            if quantity <= 0:
                continue

            item = Item.objects.get(id=item_id)

            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                item=item,
                defaults={"quantity": quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        return redirect("items:items_list")
    
def cart_list(request):
    cart_items = CartItem.objects.select_related("item").filter(user=request.user)
    total_price = sum(ci.item.price * ci.quantity for ci in cart_items)

    return render(
        request,
        "cart/cart-list.html",
        {
            "cart_items": cart_items,
            "total_price": total_price,
        }
    )