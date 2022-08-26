
from django.contrib import admin
from weather.levels.models import Level


@admin.register(Level)
class AdminLevel(admin.ModelAdmin):
    list_display = ('id', 'description', )
