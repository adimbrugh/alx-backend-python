from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Prefetch
from messaging.models import Message



@login_required
def delete_user(request):
    user = request.user
    logout(request)  # log them out before deletion
    user.delete()
    return redirect('home')  # or wherever you want to redirect post-deletion



def get_conversation_with_threads(request, other_user_id):
    messages = Message.objects.filter(
        sender=request.user,
        receiver__id=other_user_id,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).order_by('timestamp')

    return messages



def fetch_thread(message):
    """ Recursively fetch all nested replies to a message """
    thread = []
    replies = message.replies.all().select_related('sender', 'receiver')
    for reply in replies:
        thread.append({
            'message': reply,
            'replies': fetch_thread(reply)  # recurse
        })
    return thread



@login_required
def unread_inbox_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender', 'timestamp', 'content'
    )  # Uses the custom manager + optimized .only()

    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages
    })
    
    
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Conversation


@cache_page(60)  # 60 seconds cache
def conversation_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).select_related('sender')

    return render(request, 'chats/conversation.html', {
        'conversation': conversation,
        'messages': messages
    })