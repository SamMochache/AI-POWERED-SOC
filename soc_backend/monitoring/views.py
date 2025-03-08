import numpy as np
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Log, Threat, Alert
from django.contrib.auth.models import User
from .serializers import LogSerializer, ThreatSerializer, AlertSerializer
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse 
from django.shortcuts import render
from sklearn.ensemble import IsolationForest
from datetime import timedelta


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

def extract_features():
    logs = Log.objects.all().values("source_ip", "destination_ip", "protocol", "timestamp")
    
    data = []
    for log in logs:
        data.append([
            int(log["source_ip"].split(".")[-1]),  # Convert last octet of IP to numerical feature
            int(log["destination_ip"].split(".")[-1]),
            hash(log["protocol"]) % 1000,  # Convert protocol into a numeric representation
            log["timestamp"].timestamp(),  # Convert timestamp to a numerical format
        ])
    
    return np.array(data)

def detect_anomalies():
    # Extract network traffic features
    data = extract_features()
    
    if len(data) == 0:
        print("No data available for anomaly detection")
        return

    # Train Isolation Forest Model
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(data)

    # Predict anomalies (-1 indicates anomaly)
    predictions = model.predict(data)

    # Identify anomalous logs
    anomalies = [i for i, pred in enumerate(predictions) if pred == -1]

    # Generate alerts for detected anomalies
    for index in anomalies:
        log = Log.objects.all()[index]  # Fetch the corresponding log entry
        user = User.objects.first()  # Assign alert to the first user (modify as needed)
        Alert.objects.create(user=user, message=f"Anomaly detected: {log}")

    print(f"🔍 {len(anomalies)} anomalies detected and alerts created.")

