""" Django models utilities """

# Django
from django.db import models


class HobbifyModel(models.Model):
    """
    Hobbify's base model.
    HobbifyModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    is_hidden = models.BooleanField(
        'hidden',
        default=False,
        help_text=(
            'Due to system requirements a database entry cannot be deleted. '
            'Hidden represents deleted for the users.'
        )
    )

    class Meta:
        """ Meta option """

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
