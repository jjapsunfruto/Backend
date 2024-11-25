from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from KKaebiBack.utils import (
    calculate_today_completion_rate,
    calculate_weekly_completion_rate,
    calculate_level
)
from User.models import User
from Housework.models import Housework
from datetime import date, timedelta  # timedelta 임포트 추가


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house
        housename = house.housename if house else "No House"

        # 오늘 완료율 계산
        today_completion_rate = calculate_today_completion_rate(user)

        # 일주일 완료율 및 레벨 계산
        weekly_completion_rate = calculate_weekly_completion_rate(user)
        level = calculate_level(weekly_completion_rate)

        response_data = {
            "house": housename,
            "nickname": user.nickname,
            "tasks": {
                "today_completion_rate": f"{today_completion_rate}%",
                "weekly_completion_rate": f"{weekly_completion_rate}%",
                "level": level
            }
        }
        return Response(response_data, status=200)


class HomeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 일주일 레벨 계산
        weekly_completion_rate = calculate_weekly_completion_rate(user)
        level = calculate_level(weekly_completion_rate)

        # 사용자 전체 할 일 정보
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

        return Response({"details": tasks_info, "level": level}, status=200)


class FamilyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house

        if not house:
            return Response({"message": "User is not part of any house."}, status=400)

        # 사용자 통계 (오늘 기준)
        today_completion_rate = calculate_today_completion_rate(user)
        user_completion_status = (
            f"{today_completion_rate}%" if today_completion_rate > 0 else "오늘 할 일이 없어요"
        )

        # 가족 구성원 통계 (오늘 기준)
        family_members = User.objects.filter(house=house).exclude(id=user.id)
        family_info = []
        for member in family_members:
            member_today_completion_rate = calculate_today_completion_rate(member)
            member_completion_status = (
                f"{member_today_completion_rate}%" if member_today_completion_rate > 0 else "오늘 할 일이 없어요"
            )

            family_info.append({
                "nickname": member.nickname,
                "character": member.userCharacter,
                "today_completion_rate": member_completion_status,
            })

        return Response({
            "user": {
                "nickname": user.nickname,
                "today_completion_rate": user_completion_status,  # 오늘 기준
            },
            "family": family_info
        }, status=200)



class DistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        house = user.house

        # 달력을 기준으로 월요일 시작, 일요일 끝 계산
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # 월요일
        end_of_week = start_of_week + timedelta(days=6)  # 일요일

        # 일주일 기준 집안일 필터링
        houseworks = Housework.objects.filter(user__house=house, houseworkDate__range=[start_of_week, end_of_week])
        total_house_tasks = houseworks.count()

        # 구성원별 분배 비율 계산
        members = User.objects.filter(house=house)
        distribution = []
        for member in members:
            member_tasks = houseworks.filter(user=member).count()
            distribution_percentage = (
                int((member_tasks / total_house_tasks * 100))
                if total_house_tasks > 0 else 0
            )
            distribution.append({
                "nickname": member.nickname,
                "total_tasks": member_tasks,
                "distribution_percentage": f"{distribution_percentage}%"
            })

        return Response({
            "house": house.housename,
            "total_house_tasks": total_house_tasks,
            "distribution": distribution
        }, status=200)
