

from rest_framework import viewsets, permissions, status, filters 
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    # Add filtering by title
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    # Add filtering by conversation ID
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__conversation_id']
    
    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant in this conversation.")
        #if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
        #   raise permissions.PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
