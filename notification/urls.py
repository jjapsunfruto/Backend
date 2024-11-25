from django.urls import path
from .views import NotificationListView

app_name = 'notification'

urlpatters = [
    path('list/', NotificationListView.as_view(), name='notification-list'),
]