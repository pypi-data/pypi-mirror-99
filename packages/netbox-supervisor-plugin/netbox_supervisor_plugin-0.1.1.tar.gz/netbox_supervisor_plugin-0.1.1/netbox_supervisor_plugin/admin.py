from django.contrib import admin
from .models import Supervisor, SupervisorTenant


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    """Administrative view for Supervisor."""
    list_display = ('sid', 'name', 'email', 'phone', 'status', 'comments', 'is_active')


@admin.register(SupervisorTenant)
class SupervisorTenantAdmin(admin.ModelAdmin):
    """Administrative view for SupervisorTenant."""
    list_display = ('supervisor', 'tenant')
