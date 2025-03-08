import json
import os
from monitoring.models import Log

EVE_LOG_FILE = "/var/log/suricata/eve.json"

def parse_suricata_logs():
    if not os.path.exists(EVE_LOG_FILE):
        print(f"Log file {EVE_LOG_FILE} not found!")
        return

    with open(EVE_LOG_FILE, "r") as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                if "alert" in log_entry:
                    Log.objects.create(
                        timestamp=log_entry["timestamp"],
                        source_ip=log_entry["src_ip"],
                        destination_ip=log_entry["dest_ip"],
                        protocol=log_entry["proto"],
                        status="alert"
                    )
                    print(f"Logged alert from {log_entry['src_ip']} to {log_entry['dest_ip']}")
            except json.JSONDecodeError:
                continue
