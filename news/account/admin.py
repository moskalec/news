from .models import Profile, Contact
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User

admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
