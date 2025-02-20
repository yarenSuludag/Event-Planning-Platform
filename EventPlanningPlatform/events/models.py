from django.db import models
from users.models import CustomUser
from django.apps import apps  # apps.get_model() için


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=50)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participants = models.ManyToManyField(CustomUser, related_name='participated_events')
    is_approved = models.BooleanField(default=False)  # Onay durumu ekleniyor

    # Yeni alanlar
    created_at = models.DateTimeField(auto_now_add=True)  # Etkinlik oluşturulma zamanı
    updated_at = models.DateTimeField(auto_now=True)      # Etkinlik güncellenme zamanı

    # Yeni etkinlik bitiş zamanı özelliği
    @property
    def end_time(self):
        return self.date + self.duration

    def __str__(self):
        return self.name
    def get_participants(self):
        """
        Katılımcılar modelini almak için
        """
        CustomUser = apps.get_model('users', 'CustomUser')
        return CustomUser.objects.filter(events=self)