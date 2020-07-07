""" Recurrent instances of an habit admin models """

# Django
from django.contrib import admin

# Models
from hobbify.recurrences.models import RecurrentInstance


@admin.register(RecurrentInstance)
class RecurrenceAdmin(admin.ModelAdmin):
    """ Recurrence admin model """

    list_display = ('habit', 'done', 'is_hidden', 'created', 'modified')
    search_fields = ('habit__id',)
