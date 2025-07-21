

from rest_framework import permissions



class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of a conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Conversation objects
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # For Message objects (ensure the message belongs to a conversation the user is part of)
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        return False





"""
class IsParticipantOrSender(permissions.BasePermission):

    #Custom permission to only allow users to access their own conversations/messages.
    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        if hasattr(obj, 'sender'):
            return obj.sender == user

        return False
"""