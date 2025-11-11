from django.urls import path
from .views import hello_api, ChatAPIView

urlpatterns = [
    path('hello/', hello_api, name='hello'),
    path('chat/', ChatAPIView.as_view(), name='chat')
]