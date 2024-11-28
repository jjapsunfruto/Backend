from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, HouseStatsSerializer, HouseworkSerializer
from User.models import User
from Housework.models import Housework
from datetime import date, timedelta
from Housework.serializers import HouseworkSerializer
from KKaebiBack.utils import calculate_today_completion_rate, calculate_weekly_completion_rate, calculate_level




class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house
        housename = house.housename if house else "No House"

        user_data = UserSerializer(user).data
        selected_tags = user.houseworkTag.all()
        tags_info = [{"id": tag.id, "name": tag.tag} for tag in selected_tags]

        response_data = {
            "house": housename,
            "nickname": user.nickname,
            "userCharacter": user.userCharacter,
            "tasks": user_data,
            "selected_tags": tags_info,
        }
        return Response(response_data, status=200)
    

class HomeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 사용자 전체 할 일 정보
        my_tasks = Housework.objects.filter(user=user)

        # 직렬화된 데이터 생성
        tasks_info = HouseworkSerializer(my_tasks, many=True).data

        # 주간 완료율 및 레벨 계산
        weekly_completion_rate = calculate_weekly_completion_rate(user)
        level = calculate_level(weekly_completion_rate)

        return Response({
            "details": tasks_info,
            "level": level
        }, status=200)



class FamilyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house
        if not house:
            return Response({"message": "User is not part of any house."}, status=400)

        user_data = UserSerializer(user).data
        family_members = User.objects.filter(house=house).exclude(id=user.id)
        family_data = UserSerializer(family_members, many=True).data

        return Response({
            "user": user_data,
            "family": family_data
        }, status=200)


class DistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house
        if not house:
            return Response({"message": "User does not belong to a house."}, status=400)

        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        houseworks = Housework.objects.filter(user__house=house, houseworkDate__range=[start_of_week, end_of_week])
        members = User.objects.filter(house=house)

        house_stats = HouseStatsSerializer({'houseworks': houseworks, 'members': members}).data

        return Response({
            "house": house.housename,
            "total_house_tasks": houseworks.count(),
            "total_members": members.count(),
            **house_stats
        }, status=200)
