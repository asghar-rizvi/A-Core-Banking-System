from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate
import json
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['username'], 
                email=data['email'],
                password=data['password'],
                phone=data['phone']
            )
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        return JsonResponse(request.user.token_payload)