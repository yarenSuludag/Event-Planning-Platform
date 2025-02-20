# messaging/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from events.models import Event

@login_required(login_url='login')
def chat_list(request):
    # Kullanıcının katıldığı etkinlikleri listele
    events = Event.objects.filter(participants=request.user)
    
    # Her etkinlik için mesaj sayısını hesapla
    event_message_counts = {}
    for event in events:
        message_count = Message.objects.filter(event=event).count()  # Etkinlikteki mesaj sayısı
        event_message_counts[event.id] = message_count

    return render(request, 'chat_list.html', {'events': events, 'event_message_counts': event_message_counts})

@login_required(login_url='login')
def event_chat(request, event_id):
    # Belirli bir etkinliğin mesajlarını gösterme
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender=request.user, event=event, message_text=message_text)
            messages.success(request, 'Mesaj başarıyla gönderildi.')
        return redirect('event_chat', event_id=event_id)
    messages_list = Message.objects.filter(event=event).order_by('timestamp')
    return render(request, 'event_chat.html', {'event': event, 'messages': messages_list})
