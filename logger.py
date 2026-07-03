# logger.py
import csv
import os
from datetime import datetime

LOG_FILE = "focus_log.csv"

def log_distraction(event_type):
    now = datetime.now()
    file_exists = os.path.exists(LOG_FILE)
    
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'time', 'hour', 'event_type'])
        writer.writerow([
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M:%S'),
            now.hour,
            event_type
        ])
    print(f"[LOG] {event_type} at {now.strftime('%H:%M:%S')}")