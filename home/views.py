from KKaebiBack.utils import calculate_level
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from User.models import User, House
from Housework.models import Housework


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house
        housename = house.housename if house else "No House"

        my_tasks = Housework.objects.filter(user=user)
        total_tasks = my_tasks.count()
        completed_tasks = my_tasks.filter(houseworkDone=True).count()
        completion_rate = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
        level = calculate_level(completion_rate)

        response_data = {
            "house": housename,
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "completion_rate": f"{completion_rate}%",
                "level": level
            }
        }
        return Response(response_data, status=200)


class HomeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        my_tasks = Housework.objects.filter(user=user)
        tasks_info = [
            {
                "houseworkId": task.houseworkId,
                "tag": task.tag.tag if task.tag else None,
                "houseworkDate": task.houseworkDate,
                "houseworkPlace": task.houseworkPlace,
                "houseworkDetail": task.houseworkDetail,
                "houseworkDone": task.houseworkDone
            }
            for task in my_tasks
        ]

        return Response({"details": tasks_info}, status=200)


class FamilyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house

        if not house:
            return Response({"message": "User is not part of any house."}, status=400)

        my_tasks = Housework.objects.filter(user=user)
        total_tasks = my_tasks.count()
        completed_tasks = my_tasks.filter(houseworkDone=True).count()
        user_completion_rate = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
        user_level = calculate_level(user_completion_rate)

        family_members = User.objects.filter(house=house).exclude(id=user.id)
        family_info = []
        for member in family_members:
            family_tasks = Housework.objects.filter(user=member)
            total_family_tasks = family_tasks.count()
            completed_family_tasks = family_tasks.filter(houseworkDone=True).count()
            family_completion_rate = (
                int((completed_family_tasks / total_family_tasks * 100)) 
                if total_family_tasks > 0 else 0
            )
            family_level = calculate_level(family_completion_rate)

            family_info.append({
                "nickname": member.nickname,
                "character": member.userCharacter,
                "completion_rate": f"{family_completion_rate}%",
                "level": family_level
            })

        return Response({
            "user": {
                "nickname": user.nickname,
                "completion_rate": f"{user_completion_rate}%",
                "level": user_level
            },
            "family": family_info
        }, status=200)
    


class DistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house

        houseworks = Housework.objects.filter(user__house=house)
        total_house_tasks = houseworks.count()

        #구성원별 분배 비율 계산
        members = User.objects.filter(house=house)
        distribution = []
        for member in members:
            member_tasks = houseworks.filter(user=member).count()
            distribution_percentage = (
                int((member_tasks / total_house_tasks * 100))
                if total_house_tasks > 0 else 0
            )
            distribution.append({
                "nickname":member.nickname,
                "total_tasks":member_tasks,
                "distribution_percentage": f"{distribution_percentage}%"
            })

        return Response({
            "house" : house.housename,
            "total_house_tasks": total_house_tasks,
            "distribution":distribution
        }, status = 200)
