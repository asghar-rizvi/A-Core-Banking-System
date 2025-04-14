from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
import json
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            serializer = UserSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse(serializer.errors, status=400)
            
            user = User.objects.create_user(
                username=data.get('username', data['email']),  
                email=data['email'],
                password=data['password'],
                phone=data['phone']
            )
            
  
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'user': UserSerializer(user).data, 
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=201)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = authenticate(
                username=data.get('username', data.get('email')), 
                password=data['password']
            )
            
            if not user:
                raise exceptions.AuthenticationFailed('Invalid credentials')
                
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
            
        return JsonResponse(UserSerializer(request.user).data)