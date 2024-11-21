from django.db import models
from django.conf import settings

from User.models import User

class HouseworkTag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

class House(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_housework')
    tag = models.ForeignKey(HouseworkTag, on_delete=models.CASCADE, related_name='user_housework')

    houseworkId = models.AutoField(primary_key=True)
    houseworkDate = models.DateField('date published', auto_now_add=True)
    houseworkPlace = models.CharField(max_length=100, Null=True)
    houseworkDetail = models.CharField(max_length=100, Null=True)
    houseworkDone = models.BooleanField(default=True)

    def __str__(self):
        return self.houseworkId