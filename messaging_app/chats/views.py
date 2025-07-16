from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

# -----------------------
# Conversation ViewSet
# -----------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Add creator as a participant automatically
        conversation.participants.add(self.request.user)
        conversation.save()

# -----------------------
# Message ViewSet
# -----------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the user is a participant in the conversation
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            return Response({"detail": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)
