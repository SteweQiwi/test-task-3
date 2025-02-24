from django.contrib import admin
from messaging.models import Message, Thread

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant1', 'participant2', 'created', 'modified')
    search_fields = ('participant1__username', 'participant2__username')
    list_filter = ('created', 'modified')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'sender', 'text', 'created')
    search_fields = ('sender__username', 'text')
    list_filter = ('created',)
