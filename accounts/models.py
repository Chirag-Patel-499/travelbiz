from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import os

def user_profile_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.username}_profile.{ext}"
    return os.path.join("users/profile_images/", filename)

class User(AbstractUser):

    class Roles(models.TextChoices):
        TRAVELLER = "traveller", _("Traveller")
        VENDOR = "vendor", _("Vendor")
        ADMIN = "admin", _("Admin")

    # New fields
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.TRAVELLER
    )

    phone = models.CharField(max_length=15, blank=True, null=True)

    profile_image = models.ImageField(
        upload_to=user_profile_upload,
        blank=True,
        null=True,
        default="users/default_profile.png"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
