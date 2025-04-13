from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/users/register/', '/users/login/']:
            return self.get_response(request)

        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(request)
            user = jwt_auth.get_user(validated_token)
            request.user = user
        except (InvalidToken, AuthenticationFailed) as e:
            return JsonResponse({'error': str(e)}, status=401)
        except Exception as e:
            return JsonResponse({'error': 'Authentication failed'}, status=401)

        return self.get_response(request)