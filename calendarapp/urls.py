from django.urls import path
from .views import CalendarView


app_name = 'calendar'

urlpatterns = [
    path('<int:year>/<int:month>/', CalendarView.as_view()),
]