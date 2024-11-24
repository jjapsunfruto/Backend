from django.db import models
from django.contrib.auth.models import AbstractUser

import random, string

def housecode():
    while True:
        housecode = ''.join(random.choices(string.digits, k=4))
        if not House.objects.filter(housecode=housecode).exists():
            return housecode

class House(models.Model):
    housecode=models.IntegerField(unique=True, null=False, default=housecode)
    housename=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.housename}"

class User(AbstractUser):
    nickname=models.CharField(max_length=8)
    userCharacter=models.IntegerField(default=1)
    house = models.ManyToManyField(House, related_name='house')
    
    def __str__(self):
        return f"{self.nickname}"
