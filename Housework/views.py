from django.shortcuts import render, get_object_or_404
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import HouseworkTag
from .serializers import HouseworkSerializer

class HouseworkPostView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer=HouseworkSerializer(data=request.data)

        if serializer.is_valid():
            tag_id = request.data.get('tag')
            housework_tag = get_object_or_404(HouseworkTag, id=tag_id)
            serializer.save(user=request.user, tag=housework_tag)
            return Response({'message':'Housework post 성공', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'messange':'Housework post 실패', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
