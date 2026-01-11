from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from cart.models import CartItem

###_____________________ Customer views ###_______________________________________________
@login_required
def items_list(request):
    items = Item.objects.all()

    # Get current user's cart
    cart_items = CartItem.objects.filter(user=request.user)
    cart_dict = {ci.item.id: ci.quantity for ci in cart_items}

    for item in items:
        # Adjust qty_choices by subtracting cart quantity
        already_in_cart = cart_dict.get(item.id, 0)
        max_available = max(item.stock - already_in_cart, 0)
        item.qty_choices = range(0, max_available + 1)  # inclusive of max_available

    # Search
    query = request.GET.get("q")
    if query:
        items = items.filter(name__icontains=query)

    # Sort
    sort_by = request.GET.get("sort_by")
    if sort_by in ["name", "-name", "price", "-price"]:
        items = items.order_by(sort_by)

    # Cart summary
    cart_total = sum(ci.item.price * ci.quantity for ci in cart_items)

    return render(
        request,
        "items/items_list.html",
        {
            "items": items,
            "cart_items": cart_items,
            "cart_total": cart_total,
        },
    )




@login_required
def search_items(request):
    query = request.GET.get("q", "")
    items = Item.objects.filter(name__icontains=query)
    return render(request, "items/items_list.html", {
        "items": items,
        "query": query
    })


@login_required
def sort_items(request):
    sort_by = request.GET.get("sort_by")  # match the <select name="sort_by">

    # Map select values to ordering
    ordering = {
        "name": "name",
        "-name": "-name",
        "price": "price",
        "-price": "-price",
    }.get(sort_by)

    items = Item.objects.all()
    if ordering:
        items = items.order_by(ordering)

    return render(request, "items/items_list.html", {"items": items})



###_____________________ Employee views ###_______________________________________________


def is_employee(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.user_type == "employee"
    )


@user_passes_test(is_employee)
def employee_inventory(request):
    items = Item.objects.all().order_by("name")
    return render(request, "items/employee_inventory.html", {"items": items})



###_____________________ Employee views ###_______________________________________________

@user_passes_test(is_employee)
def add_item(request):
    if request.method == "POST":
        Item.objects.create(
            name=request.POST["name"],
            price=request.POST["price"],
            stock=request.POST["stock"],
            image=request.FILES.get("image"),
        )
        return redirect("items:inventory")

    return render(request, "items/add_item.html")


@user_passes_test(is_employee)
def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        item.price = request.POST.get("price", item.price)
        item.stock = request.POST.get("stock", item.stock)
        if "image" in request.FILES:
            item.image = request.FILES["image"]
        item.save()

        return redirect("items:inventory")

    return render(request, "items/update_item.html", {"item": item})


@user_passes_test(is_employee)
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect("items:inventory")
