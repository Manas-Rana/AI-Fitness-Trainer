import cv2
import mediapipe as mp
import numpy as np
import time

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle
    return angle


cap = cv2.VideoCapture(0)

count = 0
stage = None
start_time = time.time()

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        try:
            landmarks = result.pose_landmarks.landmark

            # Points
            shoulder = [landmarks[11].x, landmarks[11].y]
            elbow = [landmarks[13].x, landmarks[13].y]
            wrist = [landmarks[15].x, landmarks[15].y]

            hip = [landmarks[23].x, landmarks[23].y]
            knee = [landmarks[25].x, landmarks[25].y]
            ankle = [landmarks[27].x, landmarks[27].y]

            # Angles
            elbow_angle = calculate_angle(shoulder, elbow, wrist)
            knee_angle = calculate_angle(hip, knee, ankle)

            # Push-up logic
            if elbow_angle > 160:
                stage = "UP"

            if elbow_angle < 90 and stage == "UP":
                stage = "DOWN"
                count += 1

            # Simple accuracy score
            if 70 < elbow_angle < 100:
                score = "Good"
            else:
                score = "Adjust"

            # Display angles
            cv2.putText(img, f"Elbow: {int(elbow_angle)}", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

            cv2.putText(img, f"Knee: {int(knee_angle)}", (50,80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        except:
            pass

        # Timer
        elapsed = int(time.time() - start_time)

        # Display UI
        cv2.rectangle(img, (0,0), (350,120), (0,0,0), -1)

        cv2.putText(img, f"Reps: {count}", (10,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.putText(img, f"Stage: {stage}", (10,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.putText(img, f"Score: {score}", (10,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        cv2.putText(img, f"Time: {elapsed}s", (200,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        mp_draw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("AI Fitness Trainer", img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()