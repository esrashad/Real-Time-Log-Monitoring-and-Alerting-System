import time
import json
import os
from datetime import datetime, timedelta

LOG_DIR = "/app/output/error_logs"
THRESHOLD = 10
WINDOW_MINUTES = 5

def get_recent_error_logs():
    now = datetime.now()
    window_start = now - timedelta(minutes=WINDOW_MINUTES)
    error_count = 0

    for filename in os.listdir(LOG_DIR):
        filepath = os.path.join(LOG_DIR, filename)
        try:
            with open(filepath, "r") as file:
                for line in file:
                    try:
                        log = json.loads(line.strip())
                        log_time = datetime.fromisoformat(log["timestamp"])
                        if log["level"] == "ERROR" and log_time >= window_start:
                            error_count += 1
                    except:
                        continue
        except:
            continue

    return error_count

while True:
    count = get_recent_error_logs()
    if count >= THRESHOLD:
        print(f"[ALERT] {count} ERROR logs in the last {WINDOW_MINUTES} minutes!")
    else:
        print(f"[INFO] {count} ERROR logs in the last {WINDOW_MINUTES} minutes.")
    
    time.sleep(10)  
