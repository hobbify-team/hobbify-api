""" Users admin models """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from hobbify.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """ User admin model """

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    list_filter = ('is_client', 'is_staff', 'is_hidden', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Profile admin model """

    list_display = ('user',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

admin.site.register(User, CustomUserAdmin)
