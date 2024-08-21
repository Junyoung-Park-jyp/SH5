from django.urls import path
from .views import *


app_name = 'trips'
urlpatterns = [
    path('', create_trip), 
    path('ongoing/', ongoing), 
    path('finish/', finish), 
    path('detail/<int:trip_id>', detail), 
    path('invite/', invite), 
]
