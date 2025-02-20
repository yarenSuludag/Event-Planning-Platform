from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.apps import apps  # apps.get_model() için

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    points = models.IntegerField(default=0)  # Kullanıcının puanı
    location = models.CharField(max_length=255, blank=True, null=True)  # Kullanıcının coğrafi konumu (örn. şehir)

 # Kullanıcının katıldığı etkinlikler
    events = models.ManyToManyField('events.Event', related_name='participants_of', blank=True)  # Etkinlikler

    # Add related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def update_points(self, points):
        """
        Kullanıcının puanını günceller.
        """
        self.points += points
        self.save()

    def get_events(self):
        """
        Kullanıcının katıldığı etkinlikleri almak için
        """
        Event = apps.get_model('events', 'Event')
        return Event.objects.filter(participants=self)