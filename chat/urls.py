from django.urls import path
from .views import hello_api, ChatAPIView, ChatStreamAPIView, ChatRAGStreamAPIView

urlpatterns = [
    path('hello/', hello_api, name='hello'),
    path('chat/', ChatAPIView.as_view(), name='chat'),
    path('chat/stream/', ChatStreamAPIView.as_view(), name='chat_stream' ),
    path('chat/rag/stream/', ChatRAGStreamAPIView.as_view(), name='chat_rag_stream' ),
]