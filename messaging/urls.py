from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # URL for listing all user's conversations
    path('chat/', views.conversation_list, name='conversation_list'),

    # URL for a specific chat room (using the conversation's primary key)
    path('chat/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),

    # NEW: URL for initiating a new conversation (form/search page)
    path('new/', views.start_conversation, name='start_conversation'),

    # NEW: URL to create or retrieve a conversation with a specific user
    path('start/<str:username>/', views.create_or_get_conversation, name='create_or_get_conversation'),
]