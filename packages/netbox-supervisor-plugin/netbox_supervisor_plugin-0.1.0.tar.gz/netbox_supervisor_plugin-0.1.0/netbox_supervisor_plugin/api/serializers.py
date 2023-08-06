from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField, ValidationError
from netbox_supervisor_plugin.models import SupervisorTenant, Supervisor, Tenant


# SUPER
class NestedSTenantSerializer(ModelSerializer):

    class Meta:
        model = SupervisorTenant
        fields = ['id', 'tenant']


class SupervisorSerializer(ModelSerializer):
    tenants = NestedSTenantSerializer(many=True)

    class Meta:
        model = Supervisor
        fields = ['sid', 'name', 'email', 'phone', 'status', 'comments', 'is_active', 'tenants', 'created', 'last_updated']

    def create(self, validated_data):
        tenant_data = validated_data.pop('tenants')
        supervisor = Supervisor.objects.create(**validated_data)
        for tenant in tenant_data:
            SupervisorTenant.objects.create(virtual_circuit=supervisor, **tenant)
        return supervisor


class SupervisorTenantSerializer(ModelSerializer):

    class Meta:
        model = SupervisorTenant
        fields = ['id', 'supervisor', 'tenant']
