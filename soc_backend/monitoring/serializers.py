from rest_framework import serializers
from .models import Log, Threat, Alert

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'

class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threat
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
