from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from tenancy.models import Tenant
from extras.models import ChangeLoggedModel

from .choices import VirtualCircuitStatusChoices


# SUPERVISOR
class Supervisor(ChangeLoggedModel):
    """VSupervisor model."""

    sid = models.BigIntegerField(
        primary_key=True,
        verbose_name='Код организации',
        validators=[
            MaxValueValidator(99999999),
            MinValueValidator(1),
        ],
    )
    name = models.CharField(
        max_length=64,
        verbose_name='ФИО',
    )
    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        blank=True
    )
    status = models.CharField(
        max_length=30,
        verbose_name='Статус',
        choices=VirtualCircuitStatusChoices,
        default=VirtualCircuitStatusChoices.STATUS_PENDING_CONFIGURATION,
    )
    comments = models.CharField(
        max_length=100,
        verbose_name='Комментарий',
        blank=True,
    )
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        ordering = ['sid']
        verbose_name = 'Ответственный'
        verbose_name_plural = 'Ответственные'

    def __str__(self):
        return f'{self.sid} ({self.name})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_supervisor_plugin:supervisor', args=[self.sid])


class SupervisorTenant(ChangeLoggedModel):
    """Supervisor to Tenant relationship."""

    supervisor = models.ForeignKey(
        to=Supervisor,
        on_delete=models.CASCADE,
        related_name='tenants',
        verbose_name='Ответственный',
    )
    tenant = models.OneToOneField(
        to=Tenant,
        on_delete=models.CASCADE,
        related_name='supervisor',
        verbose_name='Учреждение',
    )

    class Meta:
        ordering = ['supervisor']
        verbose_name = 'Связь ответственного'
        verbose_name_plural = 'Связи ответственных'

    def get_absolute_url(self):
        return reverse('plugins:netbox_supervisor_plugin:supervisor', args=[self.supervisor.sid])
