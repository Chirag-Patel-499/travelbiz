from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import User
import os

@receiver(pre_save, sender=User)
def auto_delete_old_profile_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_image = sender.objects.get(pk=instance.pk).profile_image
    except sender.DoesNotExist:
        return

    new_image = instance.profile_image
    if old_image != new_image:
        if old_image and os.path.isfile(old_image.path):
            os.remove(old_image.path)

@receiver(post_delete, sender=User)
def delete_profile_image_on_delete(sender, instance, **kwargs):
    if instance.profile_image and os.path.isfile(instance.profile_image.path):
        os.remove(instance.profile_image.path)
