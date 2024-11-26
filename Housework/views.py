from django.shortcuts import render, get_object_or_404
from rest_framework import views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from .models import Housework
from User.models import *
from calendarapp.models import CalendarEvent
from .serializers import HouseworkSerializer
from User.serializers import UserListSerializer

import os
from datetime import datetime
from openai import OpenAI
from django.http import JsonResponse

class HouseworkPostView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer=HouseworkSerializer(data=request.data)

        if serializer.is_valid():
            tag_id = request.data.get('tag')
            housework_tag = get_object_or_404(HouseworkTag, id=tag_id)
            serializer.save(tag=housework_tag)
            return Response({'message':'Housework post 성공', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'Housework post 실패', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HomeworkUserPostView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user=request.user
        house=House.objects.get(id=user.house.id)

        housemember=User.objects.filter(house=house)
        serializer = UserListSerializer(housemember, many=True)

        return Response({
            'message': 'UserList get 성공',
            'data': {
                'housename': house.housename,
                'housemember': serializer.data
            }
        })

    def put(self, request, format=None):
        housework_id = request.data.get('houseworkId')
        manager = request.data.get('housework_manager')

        try:
            housework = Housework.objects.get(houseworkId=housework_id)
            user = User.objects.get(id=manager)

            housework.user = user
            housework.save()

            serializer = HouseworkSerializer(housework)

            return Response({
                'message': 'Housework manager put 성공',
                'data': serializer.data
            }, status=200)

        except Housework.DoesNotExist:
            return Response({'message': '해당 housework를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'message': '해당 user를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Housework manager put 실패', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def recommend_tag_with_chatgpt(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "인증된 사용자가 아닙니다."}, status=401)

    if request.user.plan != 'premium':
        return JsonResponse({"error": "AI 추천 기능은 프리미엄 요금제를 결제해야 사용할 수 있습니다."}, status=403)

    user_input = request.GET.get('message', '')
    date_str = request.GET.get('date', '').strip()

    if not user_input or not date_str:
        return JsonResponse({"error": "No message provided"}, status=400)
    
    housework_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    day_of_week = housework_date.weekday()
    housework_entries = Housework.objects.filter(houseworkDate=housework_date)
    tags = [entry.tag.tag for entry in housework_entries if entry.tag]

    if not tags:
        return response({"error": "지정된 집안일 태그가 없습니다."}, status=400)

    prompt = f"The following are the housework tags performed on {housework_date} ({housework_date.strftime('%A')}):\n"
    prompt += "\n".join(tags)
    prompt += "\nBased on the above list of tags, what is the most frequent tag? Please give only the tag and no extra explanation."


    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0
        )
        
    
        chatgpt_response = response.choices[0].message.content
        return JsonResponse({"response": chatgpt_response})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
