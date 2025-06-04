from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt import authentication


class AuthenticationMiddlewareJWT(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        request.user = self.get_user(request)
        return self.get_response(request)

    @staticmethod
    def get_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        try:
            user = authentication.JWTAuthentication().authenticate(request)[0]
        except Exception:
            pass
        return user
