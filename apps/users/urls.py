from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AuthorizeAPIView,
    ForgotPasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    ResetPasswordAPIView,
    VerifyAPIView,
)

urlpatterns = [
    path("authorize/", AuthorizeAPIView.as_view(), name="authorize"),
    path("verify/", VerifyAPIView.as_view(), name="verify"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "forgot-password/",
        ForgotPasswordAPIView.as_view(),
        name="forgot_password",
    ),
    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset_password",
    ),
]
