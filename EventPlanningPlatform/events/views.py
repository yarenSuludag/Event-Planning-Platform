import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from django import forms
from users.models import CustomUser

# Etkinlik Formu
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'duration', 'location', 'category', 'participants','latitude', 'longitude']


from collections import defaultdict
from .models import Event
# Kullanıcıya özel etkinlik önerilerini almak için fonksiyon

def recommend_events(user):
    recommendations = []

    # 1. İlgi Alanı Uyum Kuralı: Kullanıcının ilgi alanlarına göre etkinlikleri öner.
    user_interests = user.interests.split(',')  # İlgi alanlarını virgülle ayırarak alıyoruz
    events_by_interest = Event.objects.filter(category__in=user_interests)
    recommendations.extend(events_by_interest)

    # 2. Katılım Geçmişi Kuralı: Kullanıcının katıldığı etkinlik türlerine göre öneri.
    user_past_events = user.events.all()  # Kullanıcının katıldığı etkinlikler
    past_categories = user_past_events.values_list('category', flat=True).distinct()

    # Benzer türde etkinlikleri öner
    for category in past_categories:
        similar_events = Event.objects.filter(category=category).exclude(id__in=user_past_events.values_list('id', flat=True))
        recommendations.extend(similar_events)

    # 3. Coğrafi Konum Kuralı: Kullanıcının bulunduğu konuma yakın etkinlikler öner.
    user_location = user.location
    if user_location:
        nearby_events = Event.objects.filter(location__icontains=user_location)  # Location benzerliğine dayalı arama
        recommendations.extend(nearby_events)

    # Önerileri benzersiz yapma ve sıralama
    unique_recommendations = list({event.id: event for event in recommendations}.values())
    return unique_recommendations



@login_required(login_url='login')
def create_event(request):
    users = CustomUser.objects.all()  # Tüm kullanıcıları al

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
             # Latitude ve Longitude değerlerini alıyoruz
            event.latitude = request.POST.get('latitude')
            event.longitude = request.POST.get('longitude')

            # Zaman çakışmasını kontrol et
            if is_time_conflict(event, request.user):
                messages.error(request, 'Bu etkinlik için zaman çakışması var. Lütfen farklı bir zaman dilimi seçin.')
                return render(request, 'events.html', {'form': form, 'users': users})  # Hatalı formu ve kullanıcıları tekrar göster
            
            event.save()  # Etkinlik kaydedilir
            form.save_m2m()  # ManyToMany alanlarını kaydetmek için

            # Etkinlik oluşturulduktan sonra 15 puan eklenir
            request.user.update_points(15)  # Kullanıcıya 15 puan ekle

            messages.success(request, 'Etkinlik başarıyla oluşturuldu. 15 puan kazandınız.')
            return redirect('events')  # Etkinlikler sayfasına yönlendir
        else:
            messages.error(request, 'Etkinlik oluşturulurken bir hata oluştu.')
            return render(request, 'events.html', {'form': form, 'users': users})  # Hatalı formu ve kullanıcıları tekrar göster
    else:
        form = EventForm()
        return render(request, 'events.html', {'form': form, 'users': users})  # GET isteği için kullanıcıları ekle

###############################

@login_required(login_url='login')
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    # Zaman çakışması kontrolü
    if is_time_conflict(event, user):
        messages.error(request, 'Zaman çakışması! Bu etkinliğe katılamazsınız.')
        return redirect('events')  # Katılım gerçekleşmezse etkinlikler sayfasına yönlendir

    # Katılma işlemi
    if user not in event.participants.all():
        event.participants.add(user)  # Kullanıcıyı etkinliğe ekle
        user.events.add(event)  # Etkinlik kaydını kullanıcıya ekle
        
        # Puan ekleme (katılım puanı)
        user.update_points(10)  # Katılım puanı
        messages.success(request, f'{event.name} etkinliğine katıldınız. 10 puan kazandınız.')

        # İlk katılım bonusu
        if event.date and not user.events.filter(id=event.id).exists():
            user.update_points(20)  # İlk etkinlik katılımı bonusu
            messages.success(request, 'İlk etkinlik katılımınız için bonus puan kazandınız!')
    else:
        messages.info(request, f'Siz zaten {event.name} etkinliğine katıldınız.')

    return redirect('events')  # Etkinlikler sayfasına yönlendir



##########################

def is_time_conflict(event, user):
    """
    Bu fonksiyon, kullanıcının katıldığı etkinliklerin başlangıç ve bitiş zamanlarını alarak,
    yeni etkinlik ile çakışıp çakışmadığını kontrol eder.
    """
    # Kullanıcının katıldığı etkinlikleri al
    user_events = user.events.all()

    # Yeni etkinliğin başlangıç ve bitiş zamanlarını al
    new_event_start = event.date
    new_event_end = event.end_time

    # Kullanıcının katıldığı etkinliklerin zamanları ile karşılaştır
    for user_event in user_events:
        existing_event_start = user_event.date
        existing_event_end = user_event.end_time

        # Çakışma kontrolü: Yeni etkinlik mevcut etkinlik ile çakışıyor mu?
        if (new_event_start < existing_event_end and new_event_end > existing_event_start):
            return True  # Zaman çakışması var

    return False  # Çakışma yok



##############################################
from django.contrib.auth import get_user_model
from users.models import CustomUser  # CustomUser modelini import et

@login_required(login_url='login')
def event_list(request):
    user = request.user  # 'user' burada zaten CustomUser nesnesi
    events = Event.objects.all()  # Tüm etkinlikleri al
    user_events = user.events.all()  # Kullanıcının katıldığı etkinlikler (CustomUser'dan ManyToMany ile alınan etkinlikler)
    users = CustomUser.objects.all()  # Katılımcı kullanıcıları al
    recommended_events = recommend_events(user)  # Kişiye özel etkinlik önerilerini almak

    return render(request, 'events.html', {
        'events': events, 
        'user_events': user_events,  # Kullanıcının katıldığı etkinlikler
        'users': users, 
        'recommended_events': recommended_events
    })



from django.http import JsonResponse

@login_required(login_url='login')
def event_list_json(request):
    events = Event.objects.all().values()
    return JsonResponse(list(events), safe=False)


@login_required(login_url='login')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_lat = event.latitude
    event_lon = event.longitude

      # Koordinatları kontrol etmeden önce
    if event_lat is not None and event_lon is not None:
        map_center = {'lat': event_lat, 'lng': event_lon}
    else:
        # Varsayılan bir koordinat kullanıyoruz
        map_center = {'lat': 0, 'lng': 0}  # Eğer koordinatlar eksikse, 0,0 konumunu kullanıyoruz
    

    # Map center bilgilerini JSON formatında gönderiyoruz
    map_center = {'lat': event_lat, 'lng': event_lon}
    
    # JSON formatında template'ye geçiyoruz
    map_center_json = json.dumps(map_center)

    

    return render(request, 'events.html', {'event': event, 'map_center_json': map_center_json}) 

   

@login_required(login_url='login')
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etkinlik başarıyla güncellendi.')
            return redirect('events')  # Güncelleme sonrası etkinlikler sayfasına yönlendirme
        else:
            messages.error(request, 'Etkinlik güncellenirken bir hata oluştu.')
    
    # Eğer GET isteği ile gelindiyse veya form hatalıysa
    events = Event.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'events.html', {'form': form, 'event': event, 'events': events, 'users': users})


@login_required(login_url='login')
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Etkinlik başarıyla silindi.')
        return redirect('events')  # Etkinlik listesine yönlendir
    return render(request, 'delete_event.html', {'event': event})


import openrouteservice
from django.shortcuts import render, redirect

# OpenRouteService API ile rota planlama
def get_route(start_lat, start_lon, end_lat, end_lon, transport_mode='driving-car'):
    client = openrouteservice.Client(key='YOURAPIKEY')  # API anahtarınızı buraya ekleyin
    routes = client.directions(
        coordinates=[(start_lon, start_lat), (end_lon, end_lat)],  # Başlangıç ve varış koordinatları
        profile=transport_mode,  # Ulaşım türü ('driving-car', 'cycling-regular', 'foot-walking')
        format='geojson'
    )
    return routes

# Etkinlik için rota gösterme
@login_required(login_url='login')
def event_route(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    # Kullanıcının ve etkinliğin koordinatlarını al
    start_lat, start_lon = user.latitude, user.longitude
    end_lat, end_lon = event.latitude, event.longitude

    # Rota hesaplama
    route = get_route(start_lat, start_lon, end_lat, end_lon)

    # Rotayı harita üzerinde görselleştirmek
    return render(request, 'events.html', {'event': event, 'route': route})

from django.http import JsonResponse

@login_required(login_url='login')
def event_map(request):
    events = Event.objects.all()
    event_data = []
    for event in events:
        if event.latitude and event.longitude:
            event_data.append({
                'name': event.name,
                'latitude': event.latitude,
                'longitude': event.longitude
            })
        else:
            continue

    # JSON olarak etkinlik verilerini döndürüyoruz
    return JsonResponse(event_data, safe=False)



from googlemaps import Client as GoogleMapsClient 


gmaps = GoogleMapsClient(key='YOURAPIKEY')


def event_route(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_id = data.get('event_id')
            start_lat = data.get('start_lat')
            start_lon = data.get('start_lon')

            if not event_id or not start_lat or not start_lon:
                return JsonResponse({'error': 'Missing required data'}, status=400)

            # Etkinliği veritabanından al
            event = Event.objects.get(id=event_id)

            # Hedef konum
            end_lat = event.latitude
            end_lon = event.longitude

            # Google Maps API ile rota al
            directions_result = gmaps.directions(
                origin=(start_lat, start_lon),
                destination=(end_lat, end_lon),
                mode="driving"
            )

            if not directions_result:
                return JsonResponse({'error': 'No directions found'}, status=404)

            steps = directions_result[0]['legs'][0]['steps']
            route_steps = [
                {
                    'distance': step['distance']['text'],
                    'instructions': step['html_instructions']
                }
                for step in steps
            ]

            route_data = {
                'start_lat': start_lat,
                'start_lon': start_lon,
                'end_lat': end_lat,
                'end_lon': end_lon,
                'event_name': event.name,
                'event_location': event.location,
                'route_steps': route_steps
            }

            return JsonResponse(route_data)

        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event does not exist'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)

# Etkinlikler anasayfa görünümü
@login_required(login_url='login')
def events_home(request):
    return render(request, 'events.html')
