""" Group serializers """

# Django REST Framework
from rest_framework import serializers

# Model
from hobbify.groups.models import Group


class GroupModelSerializer(serializers.ModelSerializer):
    """ Group model serializer """

    members_limit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10
    )

    class Meta:
        """ Meta class """

        model = Group
        fields = (
            'id', 'name', 'slug_name',
            'about', 'picture', 'members',
            'verified', 'members_limit',
            'created', 'modified',
            'is_hidden'
        )
        read_only_fields = ('verified', 'created')
