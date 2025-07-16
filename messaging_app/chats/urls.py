from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Explicit DefaultRouter instance (as required)
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')  # Optional global access

# Nested router for /conversations/{conversation_id}/messages/
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),          # DefaultRouter endpoints
    path('', include(nested_router.urls)),   # Nested endpoints
]
