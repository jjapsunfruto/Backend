from django.urls import path
from .views import *

app_name = 'mypage'

urlpatterns = [
    path('user/', UserInfoView.as_view()),
    path('house/', HouseInfoView.as_view()),
    path('member/', HouseMemberInfoView.as_view()),
    path('remove-member/', RemoveMemberView.as_view()),
    path('plan-upgrade/', UpgradePlanView.as_view()),
]