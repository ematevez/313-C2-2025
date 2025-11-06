from django.contrib import admin
from django.urls import path
from .views import product_list

urlpatterns = [
    path("produto", product_list, name="product_list"),
    
]
