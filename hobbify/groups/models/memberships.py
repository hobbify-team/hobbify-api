""" Membership model """

# Django
from django.db import models

# Utilities
from hobbify.utils.models import HobbifyModel


class Membership(HobbifyModel):
    """
    Membership model
    A membership is the table that holds the relationship between
    a user and a group.
    """

    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True)

    is_admin = models.BooleanField(
        'group admin',
        default=False,
        help_text="Group admins can update the group's data and manage its members."
    )

    # Invitations
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)

    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='invited_by'
    )

    # Stats
    habits = models.PositiveIntegerField(default=0)

    # Status
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Only active users are allowed to interact in the groups.'
    )

    def __str__(self):
        """ Return username and group """
        return f'@{self.user.username} at #{self.group.slug_name}'
