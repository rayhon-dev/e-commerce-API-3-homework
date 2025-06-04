from django.db import models
from common.models import BaseModel
from users.models import User


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    default_shipping_address = models.TextField(blank=True)

    def __str__(self):
        return self.name or self.user.username

