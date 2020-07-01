""" Habits admin models """

# Django
from django.contrib import admin

# Models
from hobbify.habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """ Habit admin model """

    list_display = ('owner', 'name', 'is_private')
    search_fields = ('owner__username', 'owner__email')
