# Generated by Django 4.2.10 on 2024-04-14 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_alter_event_max_participants"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventparticipants",
            name="present",
            field=models.BooleanField(default=True, verbose_name="присутствовал"),
        ),
    ]