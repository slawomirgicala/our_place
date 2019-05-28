from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Flat(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20, default='jp2gmd')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Chore(models.Model):
    name = models.CharField(max_length=100)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
