from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, StreamingHttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from .langchain_service import ask_medical_bot, ask_medical_bot_sse
import sys, time

class ChatStreamAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response("Missing question", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            generate = ask_medical_bot_sse(question)

            def stream_response():
                for chunk in generate():
                    yield chunk
                    sys.stdout.flush()       # ✅ 強制立即輸出
                    time.sleep(0.01)         # ✅ 給 Django 緩衝機會釋放
                yield "[END]"

            response = StreamingHttpResponse(
                stream_response(),
                content_type="text/plain; charset=utf-8"
            )
            response['Cache-Control'] = 'no-cache'
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChatAPIView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'Missing question.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            answer = ask_medical_bot(question)
            return Response({'answer': answer})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
def hello_api(request):
    return JsonResponse({"message": "Hello from Django API!"})
