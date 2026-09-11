from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=150)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username