from .base import *  # noqa

ALLOWED_HOSTS = [
    "3-project.midnight-pages.uz",
    ".vercel.app",
    "localhost",
    "127.0.0.1",
    "5.182.26.14"
]

CORS_ALLOWED_ORIGINS = [
    "https://3-project.midnight-pages.uz"
]
CORS_ALLOW_CREDENTIALS = True

DEBUG = False
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ORIGIN_ALLOW_ALL = False

REST_FRAMEWORK.update(  # noqa: F405
    {"DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)}
)


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
