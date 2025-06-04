from drf_yasg import openapi
from rest_framework import status

AUTHORIZE_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="Authorize",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user_data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "phone": openapi.Schema(type=openapi.TYPE_STRING)
                        },
                    ),
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
}

VERIFY_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="Verify",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "tokens": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "refresh": openapi.Schema(
                                type=openapi.TYPE_STRING
                            ),
                            "access": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
}

LOGIN_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="Login",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
}

LOGOUT_SCHEMA_RESPONSE = {
    status.HTTP_205_RESET_CONTENT: openapi.Schema(
        title="Logout",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        },
    )
}

FORGOT_PASSWORD_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="Forgot Password",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "phone": openapi.Schema(type=openapi.TYPE_STRING),
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
}

RESET_PASSWORD_SCHEMA_RESPONSE = {
    status.HTTP_200_OK: openapi.Schema(
        title="Reset Password",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT),
            ),
            "data": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING)
                },
            ),
        },
    )
}
