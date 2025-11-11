from django.urls import path
from .views import hello_api, ChatAPIView, ChatStreamAPIView

urlpatterns = [
    path('hello/', hello_api, name='hello'),
    path('chat/', ChatAPIView.as_view(), name='chat'),
    path('chat/stream/', ChatStreamAPIView.as_view(), name='chat_stream' )
]