from django.db import models
from django.utils.timezone import now
from User.models import User

class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def time_since_created(self):
        time_delta = now() - self.created_at
        if time_delta.days >= 1:
            return f"{self.created_at.strftime('%Y-%m-%d')}"
        elif time_delta.seconds < 3600:
            return f"{time_delta.seconds // 60}분 전"
        else:
            return f"{time_delta.seconds // 3600}시간 전"

    def __str__(self):
        return f"{self.sender.nickname} -> {self.receiver.nickname}: {self.message}"
