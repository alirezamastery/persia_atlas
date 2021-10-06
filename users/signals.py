from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile


User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid='profile_creation')
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
