from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = ['/users/register', '/users/register/', '/users/login', '/users/login/']

    def __call__(self, request):
        if request.path in self.public_paths:
            return self.get_response(request)

        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)

            token = auth_header.split(' ')[1]  
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            request.user = user  

        except (InvalidToken, AuthenticationFailed) as e:
            return JsonResponse({'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'error': 'Authentication failed'}, status=401)

        return self.get_response(request)
