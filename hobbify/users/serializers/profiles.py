""" Profile serializer """

# Django REST Framework
from rest_framework import serializers

# Models
from hobbify.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """ Profile model serializer """

    class Meta:
        """ Meta class """

        model = Profile
        fields = (
            'picture',
            'biography'
        )
