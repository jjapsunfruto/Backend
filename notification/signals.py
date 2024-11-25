from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from Housework.models import Housework
from User.models import User
from notification.models import Notification



@receiver(post_save, sender=Housework)
def check_today_tasks_done(sender, instance, **kwargs):
    # 오늘 날짜 확인
    today = now().date()

    # 사용자의 오늘 날짜에 등록된 할 일
    user = instance.user
    today_tasks = Housework.objects.filter(user=user, houseworkDate=today)

    # 아직 완료되지 않은 할 일이 있다면 알림을 보내지 않음
    if today_tasks.filter(houseworkDone=False).exists():
        return

    # 오늘 할 일이 모두 완료된 경우
    house = user.house
    if house:
        family_members = User.objects.filter(house=house).exclude(id=user.id)  # 여기 수정됨
        for member in family_members:
            Notification.objects.create(
                sender=user,
                receiver=member,
                message=f"{user.nickname}님이 오늘의 할 일을 모두 완료했어요."
            )

