""" Groups permission classes """

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from hobbify.groups.models import Membership


class IsGroupAdmin(BasePermission):
    """ Allow access only to group admins """

    def has_object_permission(self, request, view, obj):
        """ Verify user has a membership in the obj """
        try:
            Membership.objects.get(
                user=request.user,
                group=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
