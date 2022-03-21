from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Follow, User


class UserAdmin(BaseUserAdmin):
    list_filter = ['is_staff']
    fieldsets = [
        (None, {'fields': ['username', 'email', 'password']}),
        (
            None,
            {
                'fields': [
                    'first_name',
                    'last_name',
                ],
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                'fields': [
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                ]
            },
        ),
    ]


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    fieldsets = [
        (None, {'fields': ['user', 'author']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'fields': [
                    'user',
                    'author',
                ]
            },
        ),
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
