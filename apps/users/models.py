import random
import uuid

from common.validators import username_validator, validate_phone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    phone = models.CharField(
        max_length=12,
        unique=True,
        validators=[validate_phone],
        null=True,
    )
    full_name = models.CharField(max_length=255, null=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @staticmethod
    def generate_code():
        return random.randint(100000, 999999)

    @staticmethod
    def add_to_cache(key, value, ttl=120):
        """If the entered key is already taken,
        then returns False
        """
        return cache.add(f"{key}", value, timeout=ttl)

    @staticmethod
    def set_to_cache(key, value, ttl=120):
        """If the entered key is already taken,
        then set the new value and time
        """
        return cache.set(f"{key}", value, timeout=ttl)

    @staticmethod
    def clear_cache(cache_key):
        cache.delete(key=cache_key)
