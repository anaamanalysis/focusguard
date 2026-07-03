# scheduler.py
import json
import os
from datetime import datetime

SCHEDULE_FILE = "schedule.json"

def load_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        # Default schedule if none set
        return [
            {"start": "09:00", "end": "11:00", "label": "Deep Work"},
            {"start": "11:30", "end": "13:00", "label": "Study"},
            {"start": "15:00", "end": "17:00", "label": "Project Work"}
        ]
    with open(SCHEDULE_FILE, 'r') as f:
        return json.load(f)

def is_focus_time():
    now = datetime.now().strftime('%H:%M')
    schedule = load_schedule()
    
    for block in schedule:
        if block['start'] <= now <= block['end']:
            return True
    return False

def get_current_block():
    now = datetime.now().strftime('%H:%M')
    schedule = load_schedule()
    
    for block in schedule:
        if block['start'] <= now <= block['end']:
            return block['label']
    return None