# detector.py
import cv2
import mediapipe as mp
from ultralytics import YOLO
import time
from logger import log_distraction
from alert import trigger_alert
from scheduler import is_focus_time

# Load models
yolo_model = YOLO('yolov8n.pt')  # nano = small and fast
mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(min_detection_confidence=0.5)

def run_detector():
    cap = cv2.VideoCapture(0)
    no_face_start = None
    print("✅ FocusGuard is watching...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Only monitor during focus time
        if not is_focus_time():
            cv2.putText(frame, "BREAK TIME - Monitoring paused", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("FocusGuard", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # --- Face Detection (are you at your desk?) ---
        face_results = face_detector.process(rgb_frame)
        face_detected = face_results.detections is not None

        if not face_detected:
            if no_face_start is None:
                no_face_start = time.time()
            elif time.time() - no_face_start > 10:  # 10 seconds away
                log_distraction("left_desk")
                trigger_alert("You left your desk!")
                no_face_start = None
        else:
            no_face_start = None

        # --- YOLO Detection (phone in hand?) ---
        yolo_results = yolo_model(frame, verbose=False)
        for result in yolo_results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = yolo_model.names[class_id]
                confidence = float(box.conf[0])

                if label == 'cell phone' and confidence > 0.5:
                    log_distraction("phone_detected")
                    trigger_alert("Put your phone down!")

                    # Draw red box around phone
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f"PHONE {confidence:.0%}", 
                               (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.6, (0, 0, 255), 2)

        # Status display on camera feed
        status = "FOCUSING ✓" if face_detected else "WHERE ARE YOU?"
        color = (0, 255, 0) if face_detected else (0, 0, 255)
        cv2.putText(frame, status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("FocusGuard", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detector()