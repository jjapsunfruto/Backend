from django.urls import path
from .views import *

app_name = 'housework'

urlpatterns = [
    path('posting/', HouseworkPostView.as_view())
]