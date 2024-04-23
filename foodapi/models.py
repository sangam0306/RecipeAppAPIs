from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=20)


class Indegridents(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)
    indegridents = models.ForeignKey(Indegridents, on_delete=models.CASCADE)
    video_urls = models.TextField(null=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
