""" Membership serializers """

# Django
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers

# Serializers
from hobbify.users.serializers import UserModelSerializer

# Models
from hobbify.groups.models import Membership, Invitation


class MembershipModelSerializer(serializers.ModelSerializer):
    """ Member model serializer """

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """ Meta class """

        model = Membership
        fields = (
            'user', 'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by', 'joined_at', 'habits',
            'created', 'modified', 'is_hidden'
        )
        read_only_fields = (
            'user',
            'used_invitations',
            'invited_by',
            'created'
        )


class AddMemberSerializer(serializers.Serializer):
    """
    Add member serializer.
    Handle the addition of a new member to a group.
    Group object must be provided in the context.
    """

    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        """ Verify user isn't already a member """
        group = self.context['group']
        user = data
        q = Membership.objects.filter(group=group, user=user)
        if q.exists():
            raise serializers.ValidationError('User is already member of this group')
        return data

    def validate_invitation_code(self, data):
        """ Verify code exists and that it is related to the group """
        try:
            invitation = Invitation.objects.get(
                code=data,
                group=self.context['group'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context['invitation'] = invitation
        return data

    def validate(self, data):
        """ Verify group is capable of accepting a new member """
        group = self.context['group']
        if group.members.count() >= group.members_limit:
            raise serializers.ValidationError('Group has reached its member limit.')
        return data

    def create(self, data):
        """ Create new group member """
        group = self.context['group']
        invitation = self.context['invitation']
        user = data['user']

        now = timezone.now()

        # Member creation
        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            group=group,
            invited_by=invitation.issued_by
        )

        # Update Invitation
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        # Update issuer data
        issuer = Membership.objects.get(user=invitation.issued_by, group=group)
        issuer.used_invitations += 1
        issuer.remaining_invitations -= 1
        issuer.save()

        return member
