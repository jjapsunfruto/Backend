from django.urls import path
from .views import *

app_name = 'housework'

urlpatterns = [
    path('posting/', HouseworkPostView.as_view()),
    path('chat/', chat_with_gpt, name='chat_with_gpt'),
]