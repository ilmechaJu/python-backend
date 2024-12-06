from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from myapp.utils.token_utils import generate_access_token, generate_refresh_token, verify_access_token
from rest_framework.views import APIView  # APIView 임포트 추가
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer

import json

@csrf_exempt
def login_view(request):
    """
    로그인 및 토큰 발행
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            access_token = generate_access_token(user.id)
            refresh_token = generate_refresh_token(user.id)
            return JsonResponse({
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def refresh_token_view(request):
    """
    Refresh Token 검증 및 Access Token 재발행
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        refresh_token = data.get('refresh_token')
        payload = verify_access_token(refresh_token)

        if payload is None:
            return JsonResponse({'error': 'Invalid or expired refresh token'}, status=401)

        new_access_token = generate_access_token(payload['user_id'])
        return JsonResponse({'access_token': new_access_token}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def secure_view(request):
    return HttpResponse("로그인한 사용자만 볼 수 있습니다.")

@permission_required('myapp.can_edit')
def edit_view(request):
    return HttpResponse("권한이 있는 사용자만 볼 수 있습니다.")

@login_required
def protected_view(request):
    return HttpResponse("이 페이지는 인증된 사용자만 접근할 수 있습니다.")

class SignupView(APIView):
    """
    회원가입 API
    """
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 