from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from categories.models import Category


class EventManager(models.Manager):
    def get_public_events(self):
        return (
            self.get_queryset()
            .select_related('author', 'category')
            .prefetch_related('participants')
        )
    
    def get_future_events(self):
        return (
            self.get_public_events()
            .filter(end__gte=timezone.now())
        )


class Event(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name='автор',
    )

    title = models.CharField(
        verbose_name='название',
        max_length=150,
    )

    description = models.TextField(
        verbose_name='описание',
    )

    created = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        verbose_name='изменено',
        auto_now=True,
    )

    end = models.DateTimeField(
        verbose_name='дата',
        help_text='Дата проведения',
        null=True,
    )

    is_private = models.BooleanField(
        verbose_name='приватное',
        help_text='Доступ из профиля',
        default=False,
    )

    is_canceled = models.BooleanField(
        verbose_name='отменено',
        default=False,
    )

    max_participants = models.PositiveIntegerField(
        verbose_name='максимальное количество участников',
        help_text=(
                'Укажите кол-во участников, или оставьте пустым'
            ),
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='EventParticipants',
        related_name='events',
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='категория',
        related_name='events',
    )

    objects = EventManager()

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return timezone.now() > self.end



class EventParticipants(models.Model):
    class StatusChoices(models.IntegerChoices):
        WILL_ATTEND = 0, 'Обязательно буду'
        DONT_KNOW = 1, 'Пока решаю'
        CANT_GO = 2, 'Не пойду'

    class RoleChoices(models.IntegerChoices):
        ADMINISTRATOR = 0, 'Администратор'
        ORGANIZER = 1, 'Организатор'
        PARTICIPANT = 2, 'Участник'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='участник',
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name='мероприятие',
    )

    created = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        verbose_name='изменено',
        auto_now=True,
    )

    status = models.PositiveSmallIntegerField(
        verbose_name='статус',
        choices=StatusChoices.choices,
        default=StatusChoices.DONT_KNOW,
    )

    present = models.BooleanField(
        verbose_name='присутствовал',
        default=True,
    )

    notified = models.BooleanField(
        verbose_name='уведомлен',
        default=False,
    )

    role = models.PositiveSmallIntegerField(
        verbose_name='роль',
        choices=RoleChoices.choices,
        default=RoleChoices.PARTICIPANT,
    )

    class Meta:
        verbose_name = 'участник мероприятия'
        verbose_name_plural = 'участники мероприятия'

    def __str__(self):
        return f'{self.event} - {self.user}'
    

@receiver(pre_save, sender=Event)
def update_notified_on_end_change(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = Event.objects.get(pk=instance.pk)
            if old_instance.end != instance.end:
                instance.eventparticipants_set.filter(notified=True).update(notified=False)
        except Event.DoesNotExist:
            pass
