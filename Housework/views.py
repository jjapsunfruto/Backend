from django.shortcuts import render, get_object_or_404
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import HouseworkTag
from .serializers import HouseworkSerializer

import os
from openai import OpenAI
from django.conf import settings
from django.http import JsonResponse

class HouseworkPostView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer=HouseworkSerializer(data=request.data)

        if serializer.is_valid():
            tag_id = request.data.get('tag')
            housework_tag = get_object_or_404(HouseworkTag, id=tag_id)
            serializer.save(user=request.user, tag=housework_tag)
            return Response({'message':'Housework post 성공', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'Housework post 실패', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def chat_with_gpt(request):
    user_input = request.GET.get('message', '')

    if not user_input:
        return JsonResponse({"error": "No message provided"}, status=400)
    
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=150,
            temperature=0
        )
        
    
        chatgpt_response = response.choices[0].message.content
        return JsonResponse({"response": chatgpt_response})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
