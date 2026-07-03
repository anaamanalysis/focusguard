# alert.py
import time

last_alert_time = 0
ALERT_COOLDOWN = 30  # seconds between alerts so it's not annoying

def trigger_alert(message):
    global last_alert_time
    now = time.time()
    
    if now - last_alert_time < ALERT_COOLDOWN:
        return  # Don't spam alerts
    
    last_alert_time = now
    print(f"\n🚨 ALERT: {message}\n")
    
    # Windows popup notification
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "FocusGuard 🎯", 0x40 | 0x1000)
    except:
        pass  # Silent fail if popup doesn't work