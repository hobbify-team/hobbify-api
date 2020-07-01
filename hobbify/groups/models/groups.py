""" Habit group model """

# Django
from django.db import models

# Utils
from hobbify.utils.models import HobbifyModel


class Group(HobbifyModel):
    """
    Group model.
    A group is a private entity in which people unites to
    follow a habit. To join a group a user must receive
    an unique invitation code from an existing group member.
    """

    name = models.CharField('group name', max_length=100)
    slug_name = models.SlugField(unique=True, max_length=20)

    about = models.CharField('group description', max_length=255)
    picture = models.ImageField(upload_to='groups/pictures', blank=True, null=True)

    members = models.ManyToManyField(
        'users.User',
        through='groups.Membership',
        through_fields=('group', 'user')
    )

    verified = models.BooleanField(
        'verified group',
        default=False,
        help_text='Verified groups are also known as official communities.'
    )

    members_limit = models.PositiveIntegerField(
        default=10,
        help_text='This will be the limit on the number of members.'
    )

    def __str__(self):
        """ Returns group name """
        return self.name
