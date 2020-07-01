""" Circles permission classes """

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from hobbify.groups.models import Membership


class IsActiveGroupMember(BasePermission):
    """
    Allow access only to group members.
    Expect that the views implementing this permission
    have a `group` attribute assigned.
    """

    def has_permission(self, request, view):
        """ Verify user is an active member of the group """

        membership = view.get_object()

        if membership.user == request.user:
            return True

        try:
            Membership.objects.get(
                user=request.user,
                group=view.group,
                is_active=True,
                is_admin=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """ Allow access only to member owners """

    def has_permission(self, request, view):
        """ Let object permission grant access """
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """ Allow access only if member is owned by the requesting user """
        return request.user == obj.user
