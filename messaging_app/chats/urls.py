from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Explicit DefaultRouter instance (as required)
routers = DefaultRouter()
routers.register('conversations', ConversationViewSet, basename='conversations')
routers.register('messages', MessageViewSet, basename='messages')  # Optional global access

# Nested router for /conversations/{conversation_id}/messages/
nested_router = NestedDefaultRouter(routers, 'conversations', lookup='conversation')
nested_router.register('messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(routers.urls)),          # DefaultRouter endpoints
    path('', include(nested_router.urls)),   # Nested endpoints
]

urlpatterns += routers.urls