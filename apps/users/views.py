from common.utils.custom_response_decorator import custom_response
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .response_schema import (
    AUTHORIZE_SCHEMA_RESPONSE,
    FORGOT_PASSWORD_SCHEMA_RESPONSE,
    LOGIN_SCHEMA_RESPONSE,
    LOGOUT_SCHEMA_RESPONSE,
    RESET_PASSWORD_SCHEMA_RESPONSE,
    VERIFY_SCHEMA_RESPONSE,
)
from .serializers import (
    AuthorizeSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    ResetPasswordSerializer,
    VerifySerializer,
)

User = get_user_model()


@custom_response
class AuthorizeAPIView(generics.GenericAPIView):
    serializer_class = AuthorizeSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=AUTHORIZE_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        User.objects.send_code(
            phone=validated_data["phone"], password=validated_data["password"]
        )
        return Response(
            {
                "user_data": validated_data,
                "message": "Verification code send success",
            }
        )


@custom_response
class VerifyAPIView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=VERIFY_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        password = validated_data.get("password")
        phone = validated_data["phone"]
        if password is None:
            return Response({"phone": phone, "message": "Success verified"})
        user = User.objects.register_user(validated_data)
        return Response(
            {"tokens": user.tokens(), "message": "Registration successful."}
        )


@custom_response
class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=LOGIN_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses=LOGOUT_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "You have successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            raise ValidationError({"message": "Invalid token"})


@custom_response
class ForgotPasswordAPIView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=FORGOT_PASSWORD_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        phone = validated_data["phone"]
        User.objects.send_code(phone)
        return Response(
            {
                "phone": validated_data["phone"],
                "message": "Verification code send success",
            }
        )


@custom_response
class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses=RESET_PASSWORD_SCHEMA_RESPONSE)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        phone = validated_data["phone"]
        user = get_object_or_404(User, phone=phone)
        user.set_password(validated_data["password"])
        user.save()
        OutstandingToken.objects.filter(user=user).delete()
        return Response(
            {
                "message": "Your password changed successfully",
            }
        )
