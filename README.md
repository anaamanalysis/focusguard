# 🎯 FocusGuard — AI Productivity & Distraction Monitor

A real-time AI system that watches you through your laptop camera, 
detects when you get distracted, and tracks your daily focus score 
over time. Built for students and remote workers who want honest, 
data-driven feedback on their attention habits.

## 🚨 What It Detects
- 📱 Phone picked up during focus time
- 🚶 You leaving your desk for more than 10 seconds
- ⏰ Schedule-aware ,only monitors during YOUR focus blocks

## 📊 What It Shows You
- Real-time alerts the moment distraction is detected
- Daily focus score (0–100) based on distraction count
- Hourly distraction timeline : when are you most distracted?
- Weekly trend — are you actually improving?
- Motivational feedback based on your session performance

## 🛠️ Tech Stack
- **OpenCV** — real-time camera access and video processing
- **YOLOv8 nano** (Ultralytics) — pretrained object detection, 
  identifies phones in live video
- **MediaPipe** (Google) — face detection, knows when you leave your desk
- **Pandas** — logs and analyses distraction events over time
- **Streamlit** — interactive focus dashboard with charts and score
- **Python** — everything runs locally, no data sent anywhere

## 🔒 Privacy First
FocusGuard runs entirely on your machine. No video is recorded, 
stored, or sent anywhere. Only distraction events (timestamp + type) 
are saved locally to a CSV file.

## 🚀 How to Run

### 1. Install dependencies
```bash
py -3.12 -m pip install opencv-python mediapipe ultralytics 
pandas streamlit
```

### 2. Start the monitor (Terminal 1)
```bash
py -3.12 detector.py
```
A camera window opens. FocusGuard is now watching.
Press **Q** to stop monitoring.

### 3. Open the dashboard (Terminal 2)
```bash
py -3.12 -m streamlit run app.py
```
Opens in your browser at localhost:8501

### 4. Set your schedule
In the dashboard sidebar, add your focus blocks 
(e.g. 9:00–11:00 Deep Work). FocusGuard only monitors 
during these times.

## 📁 Project Structure
FocusGuard/
├── detector.py      # Core engine — camera + YOLO + MediaPipe
├── logger.py        # Saves distraction events to CSV
├── scheduler.py     # Schedule logic — when to monitor
├── alert.py         # Fires alerts when distraction detected
├── app.py           # Streamlit focus dashboard
├── focus_log.csv    # Auto-created distraction log
└── requirements.txt # All dependencies

## 💡 Why I Built This
Most productivity tools tell you to focus. This one watches 
whether you actually do — and shows you the data. Built as 
a real-world computer vision project combining object detection, 
face detection, event logging, and data visualisation in one 
locally-running application.

## 👩‍💻 Author
**Anaam Bind Hussain** — BTech AI & Data Science, Final Year  
[GitHub](https://github.com/anaamanalysis) | 
[FocusGuard](http://localhost:8501/)
