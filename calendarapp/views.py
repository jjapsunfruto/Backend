from Housework.models import Housework
from Housework.serializers import HouseworkSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        tasks = Housework.objects.filter(houseworkDate__year=year, houseworkDate__month=month)
        serializer = HouseworkSerializer(tasks, many=True)
        return Response({
            'message': f"{year}-{month}의 집안일 목록입니다.",
            'data': serializer.data
            })
