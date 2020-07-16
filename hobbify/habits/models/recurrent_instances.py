""" Instance model """

# Django
from django.db import models

# Models
from hobbify.habits.models import Habit

# Utils
from hobbify.utils.models import HobbifyModel


class RecurrentInstance(HobbifyModel):
    """
    An recurrent instance is an instance of a habit that
    will follow the rrule, only past instances
    will be stored in database.
    """

    habit = models.ForeignKey(Habit, on_delete=models.SET_NULL, null=True)

    rule = models.CharField(max_length=200, null=True)
    recurrence = models.CharField(max_length=200, null=True)

    done = models.BooleanField(
        'done habit status',
        default=False,
        help_text='Used for disabling the habit or marking it as finished.'
    )

    def __str__(self):
        """ Return instance details """
        return f"Intance of habit: {self.habit.name} is done: {self.done} at {self.created}"
