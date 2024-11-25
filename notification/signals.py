from django.db.models.signals import post_save
from django.dispatch import receiver
from Housework.models import Housework
from User.models import User
from .models import Notification


@receiver(post_save, sender=Housework)
def create_notification(sender, instance, created, **kwargs):
    if instance.houseworkDone:
        house = instance.user.house
        if house:
            family_members = User.objects.filter(house=house).exclude(id=instance.user.id)
            for member in family_members:
                Notification.objects.create(
                    sender=instance.user,
                    receiver = member,
                    message = f"{instance.user.nickname}님이 할 일을 모두 완료했어요."
                )