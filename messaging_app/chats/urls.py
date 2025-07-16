from django.urls import path, include
from rest_framework.routers import DefaultRouter  # ✅ explicitly named
from .views import ConversationViewSet, MessageViewSet

# ✅ Explicit router object
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
