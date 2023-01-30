# pylint: disable=W0613
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Posts, Likes
from .serializers import UserActivitySerializer


@receiver(post_save, sender=Posts)
def save_post_creation_activity(
    sender: Posts,
    instance: Posts,
    **kwargs: dict
) -> None:
    activity_data = {
        'user': instance.user.id,
        'action': 'Post Creation'
    }
    serializer = UserActivitySerializer(data=activity_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@receiver(post_save, sender=Likes)
def save_like_action(sender: Likes, instance: Likes, **kwargs: dict) -> None:
    activity_data = {
        'user': instance.user.id,
        'action': 'Like'
    }
    serializer = UserActivitySerializer(data=activity_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@receiver(post_delete, sender=Likes)
def save_unlike_action(sender: Likes, instance: Likes, **kwargs: dict) -> None:
    activity_data = {
        'user': instance.user.id,
        'action': 'Unlike'
    }
    serializer = UserActivitySerializer(data=activity_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()


# Change behavior of User Activity table
# If User login into system save it as Type Login
# In other cases overwrite actions of User (post creation, like, unlike)
