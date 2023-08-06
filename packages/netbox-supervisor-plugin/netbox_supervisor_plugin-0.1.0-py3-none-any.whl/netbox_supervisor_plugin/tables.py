import django_tables2 as tables
from django_tables2.utils import Accessor
from utilities.tables import BaseTable, ToggleColumn

from .models import Supervisor, SupervisorTenant


class SupervisorTable(BaseTable):
    pk = ToggleColumn()
    sid = tables.LinkColumn(
        viewname='plugins:netbox_supervisor_plugin:supervisor',
        args=[Accessor('sid')]
    )

    class Meta(BaseTable.Meta):
        model = Supervisor
        fields = (
            'pk',
            'sid',
            'name',
            'email',
            'phone',
            'status',
            'comments',
            'is_active',
        )


class SupervisorTenantTable(BaseTable):
    pk = ToggleColumn()
    supervisor = tables.LinkColumn(
        viewname='plugins:netbox_supervisor_plugin:supervisor',
        args=[Accessor('supervisor.sid')]
    )
    tenant = tables.LinkColumn(
        viewname='tenancy:tenant',
        args=[Accessor('tenant.pk')]
    )

    class Meta(BaseTable.Meta):
        model = SupervisorTenant
        fields = (
            'pk',
            'supervisor',
            'tenant',
        )
