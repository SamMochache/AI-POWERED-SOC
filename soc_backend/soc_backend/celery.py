import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soc_backend.settings")

app = Celery("soc_backend")

# Load settings from Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

# Celery Beat Periodic Task Scheduling
app.conf.beat_schedule = {
    "run_anomaly_detection_every_10min": {
        "task": "monitoring.tasks.run_anomaly_detection",
        "schedule": crontab(minute="*/10"),  # Run every 10 minutes
    },
}
