from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from User.models import User, House
from Housework.models import Housework
from KKaebiBack.utils import calculate_level

class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        nickname = user.nickname
        housename = user.house.first().housename if user.house.exists() else "NO HOUSE"

        my_tasks = Housework.objects.filter(user=user)
        total_tasks = my_tasks.count()
        completed_tasks = my_tasks.filter(houseworkDone=True).count()
        completion_rate = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
        level = calculate_level(completion_rate)

        tasks_info = [
            {
                "hoseworkId": task.houseworkId,
                "tag": task.tag.tag if task.tag else None,
                "houseworkDate": task.houseworkDate,
                "houseworkPlace": task.houseworkPlace,
                "houseworkDetail": task.houseworkDetail,
                "houseworkDone": task.houseworkDone
            }
            for task in my_tasks
        ]

        house = user.house.first()
        family_members = User.objects.filter(house=house).exclude(id=user.id)

        family_info = []
        for member in family_members:
            family_tasks = Housework.objects.filter(user=member)
            total_family_tasks = family_tasks.count()
            completed_family_tasks = family_tasks.filter(houseworkDone=True).count()
            family_completion_rate = int((completed_family_tasks / total_family_tasks * 100)) if total_family_tasks > 0 else 0
            family_level = calculate_level(family_completion_rate)

            family_info.append({
                "nickname": member.nickname,
                "character": member.userCharacter,
                "completion_rate": f"{family_completion_rate}%",
                "level": family_level
            })

        response_data = {
            "house": housename,
            "level": level,
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "completion_rate": f"{completion_rate}%",
                "details": tasks_info
            },
            "family": family_info
        }

        return Response(response_data, status=200)
