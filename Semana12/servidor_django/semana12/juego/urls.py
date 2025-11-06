from django.urls import path
from .views import *

urlpatterns = [
    path("", juego_in, name="juego_in"),
    
]
