from django.urls import path
from .views import CalendarView


app_name = 'calendarapp'

urlpatterns = [
    path('date/<str:date>/', CalendarView.as_view(), name='day_view'),
]