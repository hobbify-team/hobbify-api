""" Habits serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from hobbify.habits.models import Habit
from hobbify.users.models import User

# Serializers
from hobbify.users.serializers import UserModelSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone


class HabitModelSerializer(serializers.ModelSerializer):
    """ Habit model serializer """

    owner = UserModelSerializer(read_only=True)

    class Meta:
        """ Meta detail """

        model = Habit
        fields = (
            'id', 'name', 'description',
            'end_date', 'start_date', 'is_hidden',
            'paused', 'is_private',
            'frequency', 'created', 'modified',
            'owner'
        )
    
    def validate(self, data):
        """
        Validate
        Verify that the person who is creating the habit
        is the same user making the request.
        """
        if self.context['user'] != self.context['request'].user:
            raise serializers.ValidationError('Habits mutation on behalf of others is not allowed.')

        user = self.context['user']

        return data

    def create(self, data):
        """ Create habit """
        user = self.context['user']
        habit = Habit.objects.create(**data, owner=user, paused=False, is_private=True)
        return habit
