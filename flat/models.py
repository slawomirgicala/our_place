from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# Create your models here.


def validate_nonzero(value):
    if value == 0:
        raise ValidationError(
            _('Quantity %(value)s is not allowed'),
            params={'value': value},
        )


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
    period = models.PositiveIntegerField(default=1, validators=[validate_nonzero])
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


