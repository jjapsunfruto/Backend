from django.urls import path
from .views import *

app_name = 'housework'

urlpatterns = [
    path('posting/', HouseworkPostView.as_view()),
    path('manager/', HomeworkUserPostView.as_view()),
    path('recommend-tag/', RecommendByChatGPTView.as_view(), name='recommend_tag_with_chatgpt'),
]