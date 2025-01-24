from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # after creating a new User object, also create a UserProfile object
        print(f"User profile created for {instance.username}")
        UserProfile.objects.create(user=instance)


# sender = User
# receiver = create_user_profile()
# instance = the object that is sending the signal
