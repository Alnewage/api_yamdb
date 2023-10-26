from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('role', 'bio',)})
)
admin.site.register(MyUser, UserAdmin)
