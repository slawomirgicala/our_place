from django.contrib import admin
from .models import Flat, Todo, Chore, Announcement, ChoreCounter, SpecificChore


admin.site.register(Flat)
admin.site.register(Todo)
admin.site.register(Chore)
admin.site.register(Announcement)
admin.site.register(ChoreCounter)
admin.site.register(SpecificChore)
