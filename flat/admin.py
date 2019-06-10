from django.contrib import admin
from .models import Flat, Todo, Chore, Announcement
# Register your models here.

admin.site.register(Flat)
admin.site.register(Todo)
admin.site.register(Chore)
admin.site.register(Announcement)
