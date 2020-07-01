""" Groups admin """

# Django
from django.contrib import admin

# Model
from hobbify.groups.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """ Group admin """

    list_display = (
        'slug_name',
        'name',
        'verified',
        'members_limit'
    )

    search_fields = ('slug_name', 'name')

    list_filter = (
        'verified',
        'is_hidden'
    )
