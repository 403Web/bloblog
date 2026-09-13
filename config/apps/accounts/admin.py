from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import Profile, Follow


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    readonly_fields = ('date_joined', 'updated_date', 'last_login')
    ordering = ('-date_joined',)
    list_display = (
        'email', 'id', 'is_superuser', 'is_active', 'date_joined', 'updated_date'
    )
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    search_fields = ('id', 'email')

    fieldsets = (
        ('AUTHENTICATION', {'fields': ('email', 'password')}),
        ('STATUS', {
            'fields': ('is_superuser', 'is_staff', 'is_active')
        }),
        ('PERMISSION & GROUPS', {'fields': ('user_permissions', 'groups')}),
        ('IMPORTANT DATES', {'fields': ('date_joined', 'updated_date', 'last_login')})
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email', 'password1', 'password2',
                    'is_superuser', 'is_staff', 'is_active'
                )
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'updated_date')
    list_display = ('user', 'id', 'created_date', 'updated_date')
    search_fields = ('id', 'user', 'first_name', 'last_name')


class FollowAdmin(admin.ModelAdmin):
    ordering = ('-created_date',)
    readonly_fields = ('created_date',)
    list_display = ('following', 'id', 'follower', 'created_date')
    search_fields = ('id',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
