from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation

from django.db import models
from django.contrib.auth.models import User

@login_required
def conversation_list(request):
    # Get all conversations where the current user is a participant
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')

    conversations_data = []
    for conv in conversations:
        # Get the other user by excluding the current user
        other_user = conv.participants.exclude(id=request.user.id).first()
        
        # This will be used in the template
        conversations_data.append({
            'conversation': conv,
            'other_user': other_user,
            'last_message': conv.messages.last()
        })
    return render(request, 'conversation_list.html', {'conversations_data': conversations_data})


@login_required
def conversation_detail(request, conversation_id):
    # Get the conversation or 404
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Check if the current user is a participant for security
    if request.user not in conversation.participants.all():
        return redirect('messaging:conversation_list') # Redirect if not authorized

    # Get all messages
    messages = conversation.messages.all()

    # Get the other participant's username for the chat header
    other_user = conversation.participants.exclude(id=request.user.id).first()

    context = {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
    }
    return render(request, 'conversation_detail.html', context)


@login_required
def start_conversation(request):
    """Allows the user to search for and select another user to chat with."""
    users = []
    query = request.GET.get('q')
    
    if query:
        # Search for users matching the query, excluding the current user
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(id=request.user.id)[:10] # Limit results for performance
        
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'start_conversation.html', context)


@login_required
def create_or_get_conversation(request, username):
    """Checks if a conversation already exists between two users. If not, creates one."""
    
    # Get the recipient user
    try:
        recipient = User.objects.get(username=username)
    except User.DoesNotExist:
        # Handle case where user isn't found
        # You should use Django messages here to notify the user
        return redirect('messages:start_conversation') 
    
    current_user = request.user

    # 1. Look for an existing conversation
    # Check if a conversation exists where both users are participants
    conversation = Conversation.objects.filter(
        participants=current_user
    ).filter(
        participants=recipient
    ).annotate(
        # Use a count to ensure exactly 2 participants (to exclude group chats)
        p_count=models.Count('participants') 
    ).filter(p_count=2).first() 

    if not conversation:
        # 2. If no conversation exists, create a new one
        conversation = Conversation.objects.create()
        conversation.participants.add(current_user, recipient)
        # Note: You need to add 'from django.db import models' to the top of this file
        
    # 3. Redirect to the detail view of the conversation
    return redirect('messages:conversation_detail', conversation_id=conversation.id)