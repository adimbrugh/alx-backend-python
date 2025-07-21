

from rest_framework import permissions

class IsParticipantOrSender(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own conversations/messages.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        if hasattr(obj, 'sender'):
            return obj.sender == user

        return False
