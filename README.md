# AI Fitness Trainer using Pose Estimation

##  Abstract
This project uses computer vision to detect human body posture and count push-ups in real time using a webcam.

##  Objective
- Detect human pose
- Calculate joint angles
- Count exercise repetitions
- Provide basic feedback

##  Methodology
MediaPipe Pose is used to detect body landmarks. The angle between shoulder, elbow, and wrist is calculated using trigonometric functions. Based on angle thresholds, push-up stages are detected.

##  Technologies Used
- Python
- OpenCV
- MediaPipe
- NumPy

## Features
- Real-time pose detection
- Push-up counter
- Angle calculation
- Basic accuracy feedback
- Timer tracking

## Results
The system successfully counts repetitions in real-time under proper lighting conditions.

## Limitations
- Sensitive to camera angle
- Limited to basic exercises
- No trained ML model

## Future Scope
- Add more exercises (squats, lunges)
- Improve accuracy using ML models
- Add GUI and voice feedback

## Author
Manas Rana
