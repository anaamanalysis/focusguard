# Save this as test_camera.py and run it
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    print("✅ Camera working!")
    cv2.imshow("Camera Test", frame)
    cv2.waitKey(3000)
else:
    print("❌ Camera not detected")

cap.release()
cv2.destroyAllWindows()