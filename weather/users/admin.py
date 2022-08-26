
from django.contrib import admin
from weather.users.models import User, Profile


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'email', )


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('id', 'user', 'description',)
