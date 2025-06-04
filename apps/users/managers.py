from common.exceptions import CodeResendError
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ValidationError

from .tasks import send_sms


class UserManager(BaseUserManager):
    def _create_user(
        self, password, phone=None, username=None, **extra_fields
    ):
        if phone is None and username is None:
            raise ValidationError("The given phone or username must be set")
        if username is None:
            user = self.model(phone=phone, **extra_fields)
        else:
            user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        phone = extra_fields.pop("phone", None)
        username = extra_fields.pop("username", None)
        password = extra_fields.pop("password")
        return self._create_user(
            phone=phone, username=username, password=password, **extra_fields
        )

    def create_superuser(
        self, password, phone=None, username=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", self.model.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError("Superuser must have is_superuser=True.")

        return self._create_user(
            phone=phone, username=username, password=password, **extra_fields
        )

    def send_code(self, phone: str, password=None):
        code = self.model.generate_code()
        code_add_to_cache = self.model.add_to_cache(
            key=phone, value=(code, password), ttl=60
        )
        if code_add_to_cache is False:
            raise CodeResendError

        message = f"Sizning tasdiqlash kodingiz: {code}. Ushbu kod 1 daqiqa davomida amal qiladi."
        send_sms.delay(phone=phone, text=message)

    def register_user(self, data):
        user = self.create_user(**data)
        return user
