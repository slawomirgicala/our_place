from django.db import models
from django.contrib.auth.models import User
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

