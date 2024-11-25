from django.urls import path
from .views import *

app_name = 'housework'

urlpatterns = [
    path('posting/', HouseworkPostView.as_view()),
    path('recommend-tag/', recommend_tag_with_chatgpt, name='recommend_tag_with_chatgpt'),
]