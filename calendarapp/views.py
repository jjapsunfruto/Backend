from User.models import House, User
from Housework.models import Housework
from Housework.serializers import HouseworkSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import date


class CalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        user = request.user
        tasks = Housework.objects.filter(houseworkDate__year=year, houseworkDate__month=month)
        tasks.filter(user=user)
        
        serializer = HouseworkSerializer(tasks, many=True)
        return Response({
            'message': f"{year}-{month}의 집안일 목록입니다.",
            'data': serializer.data
            })

class HouseworkDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        housework = Housework.objects.get(houseworkId=request.data.get('houseworkId'))

        if housework.user == user:

            houseworkDone = housework.houseworkDone
            if houseworkDone == True:
                housework.houseworkDone = False
            elif houseworkDone == False:
                housework.houseworkDone = True

            housework.save()
            serializer = HouseworkSerializer(housework)

            return Response({
                'message': "집안일 완료 상태 변경 완료",
                'data': serializer.data
            })

class HouseworkFamilyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month, day):
        user=request.user
        house=House.objects.get(id=user.house.id)

        housemember=User.objects.filter(house=house).exclude(id=user.id)

        target_date = date(year, month, day)
        housework=Housework.objects.filter(user__in=housemember, houseworkDate=target_date)

        serializer = HouseworkSerializer(housework, many=True)

        return Response({
            'message': "식구들의 할일 get",
            'data': serializer.data
        })