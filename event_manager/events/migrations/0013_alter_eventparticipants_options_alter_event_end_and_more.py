# Generated by Django 4.2.10 on 2024-04-27 09:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_merge_20240419_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventparticipants',
            options={'verbose_name': 'участник мероприятия', 'verbose_name_plural': 'участники мероприятия'},
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(help_text='Дата проведения', null=True, verbose_name='дата'),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_private',
            field=models.BooleanField(default=False, help_text='Доступ из профиля', verbose_name='приватное'),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_participants',
            field=models.PositiveIntegerField(blank=True, help_text='Укажите кол-во участников, или оставьте пустым', null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='максимальное количество участников'),
        ),
    ]
