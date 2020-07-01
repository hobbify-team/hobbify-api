""" Group views """

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from hobbify.groups.permissions.groups import IsGroupAdmin

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from hobbify.groups.serializers import GroupModelSerializer

# Models
from hobbify.groups.models import Group, Membership


class GroupViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """ Group model set """

    serializer_class = GroupModelSerializer
    lookup_field = 'slug_name'

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('name', 'created', 'member_limit')
    ordering = ('-members__count',)
    filter_fields = ('verified',)

    def get_queryset(self):
        """ Restrict list to non hidden groups """
        queryset = Group.objects.all()
        if self.action == 'list':
            return queryset.filter(is_hidden=False)
        return queryset

    def get_permissions(self):
        """ Assign permissions based on action """
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsGroupAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """ Assign group admin """
        group = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            group=group,
            is_admin=True,
            remaining_invitations=10
        )