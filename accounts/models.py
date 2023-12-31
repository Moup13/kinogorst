from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    image = models.ImageField(default="profile1.png", null=True, blank=True)


    def __str__(self):
        return self.username


