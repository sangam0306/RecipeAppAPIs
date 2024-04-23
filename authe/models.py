from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(null=True)
    dob = models.DateTimeField(null=True)
    description = models.TextField()
