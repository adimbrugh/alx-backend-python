from rest_framework import viewsets, permissions, status, filters  # ✅ filters added
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ✅ Add filtering by title
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ✅ Add filtering by conversation ID
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__conversation_id']

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            raise permissions.PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
