from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Log, Threat, Alert
from .serializers import LogSerializer, ThreatSerializer, AlertSerializer
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse 
from django.shortcuts import render


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

def dashboard(request):
    return render(request, 'dashboard.html')

def alert_data(request):
    last_24_hours = now() - timedelta(hours=24)
    alerts = Alert.objects.filter(created_at__gte=last_24_hours)

    data = {
        "total_alerts": alerts.count(),
        "hourly_alerts": [],
    }

    for hour in range(24):
        start_time = last_24_hours + timedelta(hours=hour)
        end_time = start_time + timedelta(hours=1)
        count = alerts.filter(created_at__range=(start_time, end_time)).count()
        data["hourly_alerts"].append(count)

    return JsonResponse(data)
