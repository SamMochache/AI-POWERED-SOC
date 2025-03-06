from django.contrib import admin
from .models import Log, Threat, Alert

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'source_ip', 'destination_ip', 'protocol', 'status')
    search_fields = ('source_ip', 'destination_ip', 'protocol')
    list_filter = ('status', 'protocol', 'timestamp')

@admin.register(Threat)
class ThreatAdmin(admin.ModelAdmin):
    list_display = ('log', 'threat_level', 'description')
    list_filter = ('threat_level',)
    search_fields = ('description',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('message',)
