from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    protocol = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=[
        ("safe", "Safe"),
        ("suspicious", "Suspicious"),
    ])

    def __str__(self):
        return f"{self.source_ip} -> {self.destination_ip} ({self.protocol})"

class Threat(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    threat_level = models.CharField(max_length=10, choices=[
        ("low", "Low"),
        ("high", "High"),
    ])
    description = models.TextField()

    def __str__(self):
        return f"Threat ({self.threat_level}): {self.description}"

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.user.username}: {self.message}"
