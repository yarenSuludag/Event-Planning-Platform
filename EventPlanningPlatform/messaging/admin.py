from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'event', 'message_text', 'timestamp')
    list_filter = ('sender', 'event', 'timestamp')
    search_fields = ('message_text', 'sender__username', 'event__name')
    ordering = ('-timestamp',)

    fieldsets = (
        (None, {'fields': ('sender', 'event', 'message_text')}),
        ('Timestamp', {'fields': ('timestamp',)}),
    )

admin.site.register(Message, MessageAdmin)
