from celery import shared_task
from monitoring.log_parser import parse_suricata_logs
from .views import detect_anomalies  # Import the detection function

@shared_task
def process_logs():
    parse_suricata_logs()
    return "Suricata logs processed!"
@shared_task
def run_anomaly_detection():
    print("🚀 Running anomaly detection...")
    detect_anomalies()