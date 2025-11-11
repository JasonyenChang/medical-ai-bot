from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .langchain_service import ask_medical_bot

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
