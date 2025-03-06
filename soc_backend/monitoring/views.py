from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Log, Threat, Alert
from .serializers import LogSerializer, ThreatSerializer, AlertSerializer

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

class ThreatViewSet(viewsets.ModelViewSet):
    queryset = Threat.objects.all()
    serializer_class = ThreatSerializer
    permission_classes = [IsAuthenticated]

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
