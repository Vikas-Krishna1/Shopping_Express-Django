from django.urls import path,include
from . import views

app_name = "items"

urlpatterns = [
    ##Authentication
      

    ##CUSTOMER
    path("", views.items_list, name="items_list"),
    path("search/", views.search_items, name="search"),
    path("sort/", views.sort_items, name="sort"),
    
    
    


    ##EMPLOYEE
     path("employee/inventory/", views.employee_inventory, name="inventory"),
    path("add/", views.add_item, name="add"),
    path("update/<int:item_id>/", views.update_item, name="update"),
    path("delete/<int:item_id>/", views.delete_item, name="delete"),

   
]
