from django.contrib import admin
from .models import Event
from django.utils.translation import gettext_lazy as _

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'category', 'created_by', 'get_participants')
    list_filter = ('date', 'category', 'created_by')
    search_fields = ('name', 'description', 'location', 'category', 'created_by__username')
    ordering = ('-date',)
    actions = ['approve_events', 'mark_as_inactive']

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = _('Participants')

    def approve_events(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected events have been approved.")
    approve_events.short_description = _('Approve selected events')

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected events have been marked as inactive.")
    mark_as_inactive.short_description = _('Mark selected events as inactive')

    fieldsets = (
        (None, {'fields': ('name', 'description', 'date', 'duration', 'location', 'category', 'created_by', 'participants')}),
        ('Status', {'fields': ('is_approved', 'is_active')}),
    )

admin.site.register(Event, EventAdmin)
