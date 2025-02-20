from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.views.generic import TemplateView
from users import views as user_views
from django.contrib.auth import views as auth_views  # Şifre sıfırlama işlemleri için auth_views eklendi
from messaging import views as messaging_views  # messaging uygulamasının görünümlerini ekleyin
from events import views as events_views  # 'events_views' olarak import ettik
router = DefaultRouter()

urlpatterns = [
    path('', user_views.home, name='home'),  # Ana sayfa
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
    path('profile/', user_views.profile, name='profile'),  # Kullanıcı profili
    path('chats/', messaging_views.chat_list, name='chat_list'),
    path('chats/<int:event_id>/', messaging_views.event_chat, name='event_chat'),
    path('api/events/', events_views.event_list_json, name='event_list_json'),
    path('event_map/', events_views.event_map, name='event_map'),  # Etkinlik haritası için URL
    path('event_route/', events_views.event_route, name='event_route'), 
    # Diğer URL'ler...
    path('join_event/<int:event_id>/', events_views.join_event, name='join_event'),  # Katılma URL'si
    # Diğer URL'ler
    path('events/<int:event_id>/route/', events_views.event_route, name='event_route'),  # Rota hesaplama URL'i
     # Diğer yollar
    path('events/', events_views.event_list, name='events'),  # Etkinlik listesini gösteren sayfa
    path('create_event/', events_views.create_event, name='create_event'),  # Yeni etkinlik oluşturma
    path('update_event/<int:event_id>/', events_views.update_event, name='update_event'),  # Etkinlik güncelleme
    path('delete_event/<int:event_id>/', events_views.delete_event, name='delete_event'),  # Etkinlik silme
    # Şifre sıfırlama URL'leri
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
