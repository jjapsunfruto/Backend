from django.db import models
from django.contrib.auth.models import AbstractUser

class House(models.Model):
    housecode=models.IntegerField(null=False)
    housename=models.CharField(max_length=100)

    def __str__(self):
        return self.housecode

class User(AbstractUser):
    nickname=models.CharField(max_length=8)
    userCharacter=models.IntegerField(default=1)
    house = models.ManyToManyField(House, related_name='house')
    
    def __str__(self):
        return self.nickname
