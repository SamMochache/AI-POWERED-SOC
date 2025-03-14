from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogViewSet, ThreatViewSet, AlertViewSet, alert_data
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'logs', LogViewSet)
router.register(r'threats', ThreatViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('alert_data/', alert_data, name='alert_data'),  # ✅ Add this

]