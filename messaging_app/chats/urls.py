

from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet, UserViewSet



# Explicit DefaultRouter instance (as required)
router = DefaultRouter()
router.register('users', UserViewSet) 
router.register('conversations', ConversationViewSet)
router.register('messages', MessageViewSet)

# Nested router for /users/{user_id}/conversations/
nested_router = NestedDefaultRouter(router, 'users', lookup='user') 
nested_router.register('conversations', ConversationViewSet, basename='user-conversations')

# Nested router for /conversations/{conversation_id}/messages/
nested_router = NestedDefaultRouter(router, 'conversations', lookup='conversation')
nested_router.register('messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),          # DefaultRouter endpoints
    path('', include(nested_router.urls)),   # Nested endpoints
]

urlpatterns += router.urls