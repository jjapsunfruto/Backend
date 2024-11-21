from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import views, status
from rest_framework_simplejwt.tokens import AccessToken

import os, requests, logging

from .models import *
from .serializers import *

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
            return JsonResponse({"message": "코드가 제공되지 않았습니다."}, status=400)

        client_id = os.environ.get('KAKAO_CLIENT_ID')
        redirect_uri = f"{KAKAO_BASE_URL}//user/login/kakao/callback/"

        token_request = requests.get(
            f"{KAKAO_URL}/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )

        token_json = token_request.json()
        logging.info(f"Kakao token response: {token_json}")

        if token_request.status_code != 200 or "access_token" not in token_json:
            return JsonResponse({"message": "INVALID_CODE"}, status=400)

        access_token = token_json["access_token"]

        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        logging.info(f"Kakao profile response: {profile_json}")

        if profile_request.status_code != 200:
            return JsonResponse({"message": "사용자 프로필 요청 실패", "error": profile_json}, status=400)

        kakao_account = profile_json.get("kakao_account")
        if kakao_account is None:
            return JsonResponse({"message": "Kakao 계정 정보가 없습니다."}, status=400)

        nickname = kakao_account.get("profile", {}).get("nickname")
        id = profile_json.get("id")

        if not nickname or not id:
            return JsonResponse({"message": "Kakao 계정 정보가 부족합니다.", "kakao_account": kakao_account, "profile_json": profile_json}, status=400)

        user, created = User.objects.get_or_create(
            id=id,
            defaults={'nickname': nickname}
        )

        token = AccessToken.for_user(user)

        return JsonResponse({"token": str(token)}, status=200)