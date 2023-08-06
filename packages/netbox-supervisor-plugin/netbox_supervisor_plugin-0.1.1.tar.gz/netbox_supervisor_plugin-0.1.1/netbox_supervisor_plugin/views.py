from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views.generic import View
from netbox.views.generic import BulkDeleteView, ObjectEditView, ObjectListView, ObjectDeleteView

from .filters import SupervisorFilter
from .forms import SupervisorForm, SupervisorTenantForm, SupervisorFilterForm
from .models import Supervisor, SupervisorTenant, Tenant
from .tables import SupervisorTable, SupervisorTenantTable


#SUPERVISOR
class SupervisorView(View):
    """Single supervisor view, identified by ID."""

    def get(self, request, pk):
        sp = get_object_or_404(Supervisor.objects.filter(sid=pk))
        tenant_ids = SupervisorTenant.objects.filter(supervisor=sp).values_list('tenant_id', flat=True)
        tenants = [Tenant.objects.get(pk=tid) for tid in tenant_ids]

        return render(request, 'netbox_supervisor_plugin/supervisor.html', {
            'supervisor': sp,
            'tenants': tenants,
        })


class SupervisorListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'netbox_supervisor_plugin.view_supervisor'
    #permission_required = 'netbox_supervisor_plugin.view_virtualcircuit'
    queryset = Supervisor.objects.all()
    filterset = SupervisorFilter
    filterset_form = SupervisorFilterForm
    table = SupervisorTable
    template_name = 'netbox_supervisor_plugin/supervisor_list.html'


class SupervisorCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'netbox_supervisor_plugin.add_supervisor'
    model = Supervisor
    queryset = Supervisor.objects.all()
    model_form =  SupervisorForm
    template_name = 'netbox_supervisor_plugin/supervisor_edit.html'
    default_return_url = 'plugins:netbox_supervisor_plugin:supervisor_list'


class SupervisorEditView(SupervisorCreateView):
    permission_required = 'netbox_supervisor_plugin.change_supervisor'


class SupervisorDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'netbox_supervisor_plugin.delete_supervisor'
    model = Supervisor
    default_return_url = 'plugins:netbox_supervisor_plugin:supervisor_list'


class SupervisorBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'netbox_supervisor_plugin.delete_supervisor'
    queryset = Supervisor.objects.filter()
    table = SupervisorTable
    default_return_url = 'plugins:netbox_supervisor_plugin:supervisor_list'


class SupervisorTenantListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'netbox_supervisor_plugin.view_supervisortenant'
    queryset = SupervisorTenant.objects.all()
    table = SupervisorTenantTable
    template_name = 'netbox_supervisor_plugin/supervisor_tenant_list.html'


class SupervisorTenantCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'netbox_supervisor_plugin.add_supervisortenant'
    model = SupervisorTenant
    queryset = SupervisorTenant.objects.all()
    model_form = SupervisorTenantForm
    template_name = 'netbox_supervisor_plugin/supervisor_tenant_edit.html'
    default_return_url = 'plugins:netbox_supervisor_plugin:supervisor_tenant_list'


class SupervisorTenantBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'netbox_supervisor_plugin.delete_supervisortenant'
    queryset = SupervisorTenant.objects.filter()
    table = SupervisorTenantTable
    default_return_url = 'plugins:netbox_supervisor_plugin:supervisor_tenant_list'

