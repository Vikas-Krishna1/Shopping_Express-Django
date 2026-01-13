from django.urls import path,include
from . import views

app_name = "items"

urlpatterns = [
    ##Authentication
      

    ##CUSTOMER
    path("", views.items_list, name="items_list"),
    path("search/", views.search_items, name="search"),
    path("sort/", views.sort_items, name="sort"),
    
    
    


    

   
]
