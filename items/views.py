from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from cart.models import CartItem
from django.contrib.auth.models import User



def home(request):
    return render(request,"items/home.html")

##AUthentication
##_____________________ Signup views ###_______________________________________________
def signupuser(request):
    if request.method == "POST":
        if request.POST["password1"] != request.POST["password2"]:
            return render(request, "items/signupuser.html", {
                "form": UserCreationForm(),
                "error": "Passwords do not match",
            })

        try:
            # Create user
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
            )

            # Set role
            role = request.POST.get("role", "CUSTOMER")
            user.profile.user_type = role
            user.profile.save()

            login(request, user)

            # Redirect based on role
            if role == "EMPLOYEE":
                return redirect("employee:dashboard")
            return redirect("items:items_list")

        except IntegrityError:
            return render(request, "items/signupuser.html", {
                "form": UserCreationForm(),
                "error": "Username already exists",
            })

    return render(request, "items/signupuser.html", {
        "form": UserCreationForm()
    })


##_____________________ Login/logout views ###_______________________________________________
def logoutuser(request):
    logout(request)
    return redirect("home")
##_______________________ LoginView ###_______________________________________________
def loginuser(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(request, "items/loginuser.html", {
                "form": AuthenticationForm(),
                "error": "Invalid credentials",
            })

        login(request, user)

        # ROLE-BASED REDIRECT
        if hasattr(user, "profile") and user.profile.user_type == "employee":
            return redirect("employee:dashboard")

        return redirect("items:items_list")

    return render(request, "items/loginuser.html", {
        "form": AuthenticationForm()
    })




###_____________________ Customer views ###_______________________________________________
##_____________________ Home page view ###_________________________________________________________________________
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



##_____________________ Search and sort views ###________________________________________________________________
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



