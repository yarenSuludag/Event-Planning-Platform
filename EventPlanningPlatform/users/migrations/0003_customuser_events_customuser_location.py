# Generated by Django 5.1.2 on 2024-11-27 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_event_participants'),
        ('users', '0002_customuser_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='events',
            field=models.ManyToManyField(related_name='participants_of', to='events.event'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
