from django.urls import path
from .views import HomeView, FamilyView, HomeDetailView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('family/', FamilyView.as_view(), name='family'),
    path('detail/', HomeDetailView.as_view(), name='home-detail'),
]
