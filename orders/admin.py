from django.contrib import admin
from .models import *
from accounts.models import *
from items.models import *
from cart.models import *
from accounts.models import *


# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Item)
admin.site.register(Address)



