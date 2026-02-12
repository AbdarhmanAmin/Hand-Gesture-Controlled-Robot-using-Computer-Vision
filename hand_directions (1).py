import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os
import serial
import time

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# ================= BLUETOOTH SETUP =================
# Change this to your ESP32 COM port
BT_PORT = "COM5"  # e.g., COM7 on Windows
BAUD_RATE = 115200

try:
    bt = serial.Serial(BT_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # wait for connection
    print(f"Connected to ESP32 on {BT_PORT}")
except:
    print("Failed to connect to ESP32 Bluetooth")
    bt = None
# ====================================================

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

last_direction = "NO GESTURE"


def getDirectionChar(direction):
    if direction == "UP":
        return "F"
    elif direction == "DOWN":
        return "B"
    elif direction == "LEFT":
        return "L"
    elif direction == "RIGHT":
        return "R"
    else:
        return "N"  # NO GESTURE


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, flipType=False)

    direction = "NO GESTURE"
    angle = 0

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        if len(lmList) >= 21:
            # Get key points
            wrist = lmList[0]  # Wrist
            index_tip = lmList[8]  # Index finger tip

            # Draw key points
            cv2.circle(frame, (wrist[0], wrist[1]), 8, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (index_tip[0], index_tip[1]), 8, (0, 255, 0), cv2.FILLED)

            # Draw line from wrist to index tip
            cv2.line(
                frame,
                (wrist[0], wrist[1]),
                (index_tip[0], index_tip[1]),
                (255, 255, 255),
                2,
            )

            # Calculate vector from wrist to index tip
            dx = index_tip[0] - wrist[0]
            dy = index_tip[1] - wrist[1]

            # Calculate angle in standard mathematical convention:
            angle = np.degrees(np.arctan2(-dy, dx))
            if angle < 0:
                angle += 360

            # Determine direction
            if (315 <= angle <= 360) or (0 <= angle < 45):
                direction = "RIGHT"
            elif 45 <= angle < 135:
                direction = "UP"
            elif 135 <= angle < 225:
                direction = "LEFT"
            elif 225 <= angle < 315:
                direction = "DOWN"

            # Draw angle visualization
            center_x, center_y = wrist[0], wrist[1]
            radius = 60

            cv2.circle(frame, (center_x, center_y), radius, (100, 100, 100), 2)

            for ref_angle, label in [
                (0, "0° (RIGHT)"),
                (90, "90° (UP)"),
                (180, "180° (LEFT)"),
                (270, "270° (DOWN)"),
            ]:
                screen_angle = -ref_angle
                if screen_angle < 0:
                    screen_angle += 360

                rad = np.radians(screen_angle)
                x_end = int(center_x + radius * np.cos(rad))
                y_end = int(center_y + radius * np.sin(rad))

                cv2.line(frame, (center_x, center_y), (x_end, y_end), (50, 50, 50), 1)

                label_x = int(center_x + (radius + 25) * np.cos(rad))
                label_y = int(center_y + (radius + 25) * np.sin(rad))
                cv2.putText(
                    frame,
                    label,
                    (label_x - 40, label_y + 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (200, 200, 200),
                    1,
                )

            screen_angle = -angle
            if screen_angle > 0:
                screen_angle += 360

            if screen_angle < 0:
                cv2.ellipse(
                    frame,
                    (center_x, center_y),
                    (radius, radius),
                    0,
                    0,
                    screen_angle,
                    (0, 255, 0),
                    3,
                )

            rad_current = np.radians(screen_angle)
            x_current = int(center_x + radius * np.cos(rad_current))
            y_current = int(center_y + radius * np.sin(rad_current))
            cv2.line(
                frame, (center_x, center_y), (x_current, y_current), (0, 255, 255), 2
            )

            cv2.putText(
                frame,
                f"Angle: {angle:.1f}°",
                (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Direction: {direction}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            print(f"Direction: {direction}, Angle: {angle:.1f}°")

    # ============ SEND DIRECTION TO ESP32 ============
    if bt and direction != last_direction:
        try:
            char = getDirectionChar(direction)
            bt.write((char).encode())
            print(f"Sent to ESP32: {direction}")
            last_direction = direction
        except:
            print("Failed to send direction via Bluetooth")
    # ================================================

    cv2.imshow("Hand Direction (90° = UP)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
if bt:
    bt.close()
cv2.destroyAllWindows()
