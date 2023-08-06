from ipam.models import VLAN
from tenancy.models import Tenant
from extras.plugins import PluginTemplateExtension

from .models import SupervisorTenant


class SupervisorCount(PluginTemplateExtension):
    model = 'tenancy.tenant'

    def right_page(self):
        # Map Supervisor' IDs to Tenants' IDs.
        m = {}
        # Filter Tenants by tenant.
        tenants = Tenant.objects.filter(name=self.context['object'])
        for t in tenants:
            # If a Tenant is presented, map back to its Supervisor to prevent duplicates.
            if SupervisorTenant.objects.filter(tenant=t).count() == 1:
                stenant = SupervisorTenant.objects.get(tenant=t)
                m[stenant.supervisor.sid] = stenant.tenant.id

        return self.render('netbox_supervisor_plugin/supervisor_tenant.html', extra_context={
            'count': len(m),
        })


template_extensions = [SupervisorCount]
