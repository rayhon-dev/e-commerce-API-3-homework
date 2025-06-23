from django.conf import settings  # ⚠️ settingsni to‘g‘ridan-to‘g‘ri import qilish kerak
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = (
            ["http"] if settings.DEBUG else ["https"]
        )
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Astrum Academy API",
        default_version="v1",
        description="API for Astrum IT Academy website",
        terms_of_service="https://www.astrum.uz/terms/",
        contact=openapi.Contact(email="info@astrum.uz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include(("users.urls", "users"), "users")),
    path("api/v1/shop/", include(("products.urls", "products"), "products")),
    path("api/v1/shop/", include(("profiles.urls", "profiles"), "profiles")),
    path("api/v1/shop/", include(("reviews.urls", "reviews"), "reviews")),
    path("api/v1/shop/", include(("cart.urls", "cart"), "cart")),
    path("api/v1/shop/", include(("orders.urls", "orders"), "orders")),

    # Swagger hamma rejimda ishlashi uchun
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]

# Static va media fayllar uchun
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Faqat development uchun toolbar
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
