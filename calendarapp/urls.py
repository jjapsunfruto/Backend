from django.urls import path
from .views import *


app_name = 'calendar'

urlpatterns = [
    path('<int:year>/<int:month>/', CalendarView.as_view()),
    path('houseworkDone/', HouseworkDoneView.as_view()),
    path('housework/my/<int:year>/<int:month>/<int:day>/', HouseworkMyView.as_view()),
    path('housework/family/<int:year>/<int:month>/<int:day>/', HouseworkFamilyView.as_view())
]