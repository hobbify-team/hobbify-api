""" Habits model """

# Django
from django.db import models

# Utils
from hobbify.utils.models import HobbifyModel
from django.utils import timezone

class Habit(HobbifyModel):
    """ Habit model """

    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=150, null=True)

    class Frequency(models.IntegerChoices):
        DAILY = 1
        WEEKLY = 2
        MONTLY = 3
        EVERY_3_DAYS = 4
        WEEKEND = 5

    frequency = models.IntegerField(default=Frequency.DAILY, choices=Frequency.choices)

    start_date = models.DateTimeField(
        'habit start date',
        null=True,
        default=timezone.now,
        help_text='Date time on which the habit is intended to start.'
    )

    end_date = models.DateTimeField(
        'habit end date',
        null=True,
        help_text='Date time on which the habit is intended to end.'
    )

    paused = models.BooleanField(
        'paused habit status',
        default=False,
        help_text='Used for disabling the habit or marking it as paused.'
    )

    done = models.BooleanField(
        'done habit status',
        default=False,
        help_text='Used for disabling the habit or marking it as finished.'
    )

    is_private = models.BooleanField(
        'private status',
        default=True,
        help_text='Set to true when the user has set a it as a private habit.'
    )

    def __str__(self):
        """ Return habit detail """
        return f'Owner: {self.owner} | {self.name}, private: {self.is_private}, done: {self.done}, paused: {self.paused}'
