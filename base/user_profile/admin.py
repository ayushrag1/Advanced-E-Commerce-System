from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


class UserProfileAdmin(UserAdmin):
    # Define fields to display in the user list view in the admin panel
    list_display = [
        'user_id', 'email', 'password', 'name', 'address',
        'phone', 'is_staff', 'is_active', 'is_superuser'
    ]
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    # Define fieldsets to control the layout in the user detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ()}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Define fields used when adding a new user via the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


# Register the CustomUser model with the custom admin class
admin.site.register(UserProfile, UserProfileAdmin)
