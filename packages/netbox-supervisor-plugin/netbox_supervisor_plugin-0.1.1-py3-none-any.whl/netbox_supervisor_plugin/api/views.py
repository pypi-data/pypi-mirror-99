from rest_framework.viewsets import ModelViewSet
from netbox_supervisor_plugin.models import SupervisorTenant, Supervisor
from .serializers import SupervisorSerializer, SupervisorTenantSerializer


class SupervisorViewSet(ModelViewSet):
    serializer_class = SupervisorSerializer

    def get_queryset(self):
        context = self.request.query_params.get('context', None)
        if context is None:
            queryset = Supervisor.objects.all().order_by('sid')
        else:
            queryset = Supervisor.objects.filter(context=context)
        return queryset


class SupervisorTenantViewSet(ModelViewSet):
    queryset = SupervisorTenant.objects.all()
    serializer_class = SupervisorTenantSerializer
