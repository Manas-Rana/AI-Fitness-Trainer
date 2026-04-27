import cv2
import mediapipe as mp
import numpy as np

# mediapipe setup
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# function to find angle between 3 points
def find_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # basic math for angle
    rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(rad * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


# starting values
count = 0
position = None

# webcam
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    while True:
        success, frame = cap.read()
        if not success:
            break

        # convert color
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(img)

        # back to BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        try:
            points = result.pose_landmarks.landmark

            # taking left arm points
            shoulder = [points[11].x, points[11].y]
            elbow = [points[13].x, points[13].y]
            wrist = [points[15].x, points[15].y]

            # calculate angle
            angle = find_angle(shoulder, elbow, wrist)

            # show angle near elbow
            cv2.putText(img, str(int(angle)),
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            # simple push-up logic
            if angle > 160:
                position = "up"

            if angle < 90 and position == "up":
                position = "down"
                count += 1

        except:
            pass

        # display box
        cv2.rectangle(img, (0,0), (250,100), (0,0,0), -1)

        cv2.putText(img, "Reps", (10,20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.putText(img, str(count), (10,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

        cv2.putText(img, "Stage", (120,20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.putText(img, str(position), (120,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        # draw pose
        mp_draw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("My Fitness Trainer", img)

        # press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()