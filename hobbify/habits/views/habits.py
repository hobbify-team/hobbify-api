""" Habits views """

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from hobbify.habits.serializers import HabitModelSerializer

# Models
from hobbify.habits.models import Habit
from hobbify.users.models import User


class HabitViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """ Habit view set """

    lookup_field = 'id'
    serializer_class = HabitModelSerializer

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ('created', 'end_date', 'start_date')
    ordering_fields = ('created', 'end_date', 'modified', 'start_date')
    search_fields = ('name', 'description')
    filter_fields = ('paused', 'is_private')

    def dispatch(self, request, *args, **kwargs):
        """ Verify that the user exists """
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(HabitViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        """ Add user to serializer context """
        context = super(HabitViewSet, self).get_serializer_context()
        context['user'] = self.user
        return context

    def get_queryset(self):
        """ Return not hidden habits """
        queryset = Habit.objects.filter(is_hidden=False)
        if self.action == 'list':
            username = self.kwargs['username']
            return Habit.objects.filter(is_hidden=False, owner__username=username)
        return queryset

    def get_permissions(self):
        """ Assign permission based on action """
        permissions = [IsAuthenticated,]
        return [p() for p in permissions]
