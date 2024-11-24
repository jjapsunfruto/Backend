from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('login/kakao/', KakaoLoginView.as_view()),
    path('login/kakao/callback/', KakaoLoginCallbackView.as_view()),
    
    path('house/', HouseInputView.as_view()),

    path('create/nickname/', NicknameCreateView.as_view()),
    path('create/house/', HouseCreateView.as_view()),
    path('create/character/', CharacterCreateView.as_view())
]