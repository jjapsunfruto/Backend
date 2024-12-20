from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken


import os, requests, logging

from .models import *
from .serializers import *
from Housework.serializers import HouseworkTagSerializer

class NicknameCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        new_nickname = request.data.get('nickname')
        user.nickname = new_nickname
        user.save() 

        serializer = UserHouseworkSerializer(user)

        return Response({
            'message': 'User의 nickname update 성공', 
            'user': serializer.data})

class HouseInputView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        housecode = request.data.get('housecode')
        user.house = House.objects.get(housecode=housecode)
        user.save()

        serializer = UserHouseworkSerializer(user)
        house = user.house
        response_data = {
            'houseid' : house.id,
            'housename' : house.housename,
            'housecode' : house.housecode
        }

        return Response({'message':'house 추가', 
                         'user':serializer.data,
                         'house':response_data
                         }, status=200)

class HouseCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        housename = request.data.get('housename')
        house = House.objects.create(housename=housename)

        user.house = house
        user.save()
        response_data = {
            'houseid' : house.id,
            'housename' : house.housename,
            'housecode' : house.housecode
        }
        return Response({'message':'house 생성', 'data':response_data}, status=status.HTTP_201_CREATED)

class CharacterCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        new_character = request.data.get('character')
        user.userCharacter = new_character
        user.save() 

        serializer = UserHouseworkSerializer(user)

        return Response({
            'message': 'User의 character update 성공', 
            'user': serializer.data})

class HouseworkTagCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user= request.user
        houseworkTag = request.data.get('houseworkTag')

        try:
            if isinstance(houseworkTag, str):
                houseworkTag = list(map(int, houseworkTag.split(',')))
        except:
            return Response({'error': "houseworkTag가 제공되지 않았습니다."})
        
        serializer = UserHouseworkSerializer(
            user, 
            data={'houseworkTag': houseworkTag}, 
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            
            return Response({
            'message': 'User의 houseworkTag update 성공',
            'user': serializer.data
            }, status=status.HTTP_200_OK)
    
        return Response({
            'message': 'User의 houseworkTag update 실패',
            'error': serializer.error
            }, status=status.HTTP_400_BAD_REQUEST)

        

KAKAO_BASE_URL = os.environ.get("KAKAO_BASE_URL")
KAKAO_URL = "https://kauth.kakao.com/oauth"

class KakaoLoginView(views.APIView):
    def get(self, request):
        client_id = os.environ.get('KAKAO_CLIENT_ID')
        redirect_uri = f"{KAKAO_BASE_URL}/user/login/kakao/callback/"
        return redirect(
            f"{KAKAO_URL}/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )

class KakaoLoginCallbackView(views.APIView):
    SECRET_KEY = os.environ.get('KAKAO_SECRET')

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"message": "코드가 제공되지 않았습니다."}, status=400)

        client_id = os.environ.get('KAKAO_CLIENT_ID')
        #redirect_uri = f"{KAKAO_BASE_URL}/user/login/kakao/callback/"
        redirect_uri = f"http://localhost:3000/accounts/kakao/callback"

        token_request = requests.get(
            f"{KAKAO_URL}/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )

        token_json = token_request.json()
        logging.info(f"Kakao token response: {token_json}")

        if token_request.status_code != 200 or "access_token" not in token_json:
            return Response({"message": "유효하지 않은 코드입니다."}, status=400)

        access_token = token_json["access_token"]

        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        logging.info(f"Kakao profile response: {profile_json}")

        if profile_request.status_code != 200:
            return Response({"message": "사용자 프로필 요청 실패", "error": profile_json}, status=400)

        kakao_account = profile_json.get("kakao_account")
        if kakao_account is None:
            return Response({"message": "Kakao 계정 정보가 없습니다."}, status=400)

        nickname = kakao_account.get("profile", {}).get("nickname")
        id = profile_json.get("id")

        if not nickname or not id:
            return Response({"message": "Kakao 계정 정보가 부족합니다.", "kakao_account": kakao_account, "profile_json": profile_json}, status=400)

        user, created = User.objects.get_or_create(
            id=id,
            defaults={'nickname': nickname}
        )

        token = AccessToken.for_user(user)

        return Response({
            "user": {
            "id": user.id,
            "nickname": user.nickname
            },
            "token": str(token)}, status=200)
