from django import forms

from utilities.forms import BootstrapMixin

from .models import VirtualCircuitStatusChoices, Supervisor, SupervisorTenant

BLANK_CHOICE = (("", "---------"),)


# SUPERVISOR
class SupervisorForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Supervisor
        fields = [
            'sid',
            'name',
            'email',
            'phone',
            'status',
            'comments',
            'is_active',
        ]


class SupervisorFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(
        required=False,
        label="Поиск",
    )
    status = forms.ChoiceField(
        choices=BLANK_CHOICE + VirtualCircuitStatusChoices.CHOICES,
        label="Статус",
        required=False
    )

    class Meta:
        model = Supervisor
        fields = [
            'q',
            'status',
            'comments',
            'email',
        ]


class SupervisorTenantForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = SupervisorTenant
        fields = [
            'supervisor',
            'tenant',
        ]
