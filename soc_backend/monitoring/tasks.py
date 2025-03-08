from celery import shared_task
from monitoring.log_parser import parse_suricata_logs

@shared_task
def process_logs():
    parse_suricata_logs()
    return "Suricata logs processed!"
