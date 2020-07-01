""" Membership views """

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from hobbify.groups.models import Group, Membership, Invitation

# Permissions
from rest_framework.permissions import IsAuthenticated
from hobbify.groups.permissions.memberships import IsActiveGroupMember, IsSelfMember

# Serializers
from hobbify.groups.serializers import MembershipModelSerializer, AddMemberSerializer


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """ Group membership view set """

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """ Verify that the group exists """
        slug_name = kwargs['slug_name']
        self.group = get_object_or_404(Group, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """ Assign permissions based on action """
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveGroupMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [permission() for permission in permissions]

    def get_queryset(self):
        """ Return group members """
        return Membership.objects.filter(
            group=self.group,
            is_active=True,
            is_hidden=False
        )

    def get_object(self):
        """ Return the group member by using the user's username """
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            group=self.group,
            is_active=True,
            is_hidden=False
        )

    def perform_destroy(self, instance):
        """ Disable membership """
        instance.is_active = False
        instance.is_hidden = True
        instance.save()

    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        """
        Retrieve a member's invitations breakdown.
        Will return a list containing all the members that have
        used its invitations and another list containing the
        invitations that haven't being used yet.
        """
        member = self.get_object()
        invited_members = Membership.objects.filter(
            group=self.group,
            invited_by=request.user,
            is_active=True,
            is_hidden=False
        )

        unused_invitations = Invitation.objects.filter(
            group=self.group,
            issued_by=request.user,
            used=False,
            is_hidden=False
        ).values_list('code')
        diff = member.remaining_invitations - len(unused_invitations)

        invitations = [x[0] for x in unused_invitations]
        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    group=self.group
                ).code
            )

        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        """ Handle member creation from invitation code """
        serializer = AddMemberSerializer(
            data=request.data,
            context={'group': self.group, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)
