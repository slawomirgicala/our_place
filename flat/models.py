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
    period = models.IntegerField()
    last_made = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ChoreCounter(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)


class SpecificChore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)


class Announcement(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Todo(models.Model):
    text = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text


