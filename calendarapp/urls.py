from django.urls import path
from .views import CalendarView, HouseworkDoneView, HouseworkFamilyView


app_name = 'calendar'

urlpatterns = [
    path('<int:year>/<int:month>/', CalendarView.as_view()),
    path('houseworkDone/', HouseworkDoneView.as_view()),
    path('houseworkMember/<int:year>/<int:month>/<int:day>/', HouseworkFamilyView.as_view())
]