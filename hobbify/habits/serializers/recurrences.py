""" Recurrences serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from hobbify.habits.models import Habit
from hobbify.users.models import User
from hobbify.habits.models import RecurrentInstance

# Serializers
from hobbify.users.serializers import UserModelSerializer
from hobbify.habits.serializers import HabitModelSerializer

# Dateutil
from dateutil.rrule import rrule, DAILY, MONTHLY, WEEKLY

# Utilities
from datetime import timedelta
from django.utils import timezone


class RecurrenceModelSerializer(serializers.ModelSerializer):
    """ Habit recurrent instance serializer """

    habit = HabitModelSerializer(read_only=True)

    class Meta:
        """ Meta details """

        model = RecurrentInstance
        fields = (
            'id', 'habit', 'rule',
            'recurrence', 'done'
        )
