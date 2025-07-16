from rest_framework import serializers
from .models import User, Conversation, Message

# -----------------------
# 1. User Serializer
# -----------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_photo',
            'is_online',
        ]

# -----------------------
# 2. Message Serializer
# -----------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'message_body',
            'sent_at',
            'is_read',
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender']

# -----------------------
# 3. Conversation Serializer (with nested messages and participants)
# -----------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'title',
            'participants',
            'messages',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']
