""" Profiles model """

# Django
from django.db import models

# Utilities
from hobbify.utils.models import HobbifyModel


class Profile(HobbifyModel):
    """ Profile model
        A profile holds a user's public data like biography, picture,
        and stadistics.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True,
    )

    biography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        """ Returns users string representation """
        return str(self.user)
