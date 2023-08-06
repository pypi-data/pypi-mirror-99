from rest_framework import routers
from .views import SupervisorViewSet, SupervisorTenantViewSet


router = routers.DefaultRouter()
router.register(r'supervisors', SupervisorViewSet, 'sid')
router.register(r'tenants', SupervisorTenantViewSet)
urlpatterns = router.urls
