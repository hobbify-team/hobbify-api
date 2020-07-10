""" Recurrences views """

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from hobbify.habits.serializers import RecurrenceModelSerializer

# Models
from hobbify.habits.models import Habit
from hobbify.users.models import User
from hobbify.habits.models import RecurrentInstance


class RecurrencesViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """ Habit recurrent instance view set """

    lookup_field = 'id'
    serializer_class = RecurrenceModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """ Verify that the user exists """
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(RecurrencesViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        """ Add user to serializer context """
        context = super(RecurrencesViewSet, self).get_serializer_context()
        context['user'] = self.user
        return context

    def get_queryset(self):
        """ Return something """
        queryset = RecurrentInstance.objects.filter(is_hidden=False)
        return queryset

    def get_permissions(self):
        """ Assign permission based on action """
        permissions = [IsAuthenticated,]
        return [p() for p in permissions]
