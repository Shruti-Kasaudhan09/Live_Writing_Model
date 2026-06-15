import cv2
import numpy as np
import mediapipe as mp

# =========================
# HAND TRACKING SETUP
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=1
)

# =========================
# SMOOTHING VARIABLES
# =========================
prev_x, prev_y = 0, 0
alpha = 0.6  # smoothing factor (higher = smoother)

# =========================
# PALM DETECTION
# =========================
def is_palm_open(hand):
    tips = [8, 12, 16, 20]
    count = 0

    for t in tips:
        if hand.landmark[t].y < hand.landmark[t - 2].y:
            count += 1

    return count >= 3

# =========================
# DRAW FUNCTION
# =========================
def draw(canvas, x1, y1, x2, y2, color, thickness):
    if x1 == 0 and y1 == 0:
        return

    cv2.line(canvas, (x1, y1), (x2, y2), color, thickness)

# =========================
# MAIN PROGRAM
# =========================
def run_air_canvas():
    global prev_x, prev_y

    cap = cv2.VideoCapture(0)
    canvas = None

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        h, w, _ = frame.shape

        pen = False
        erase = False

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)

            # =========================
            # SMOOTHING (VERY IMPORTANT FIX)
            # =========================
            x = int(prev_x * alpha + x * (1 - alpha))
            y = int(prev_y * alpha + y * (1 - alpha))

            # finger dot
            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

            # =========================
            # GESTURE DETECTION
            # =========================
            if is_palm_open(hand):
                erase = True
            else:
                if hand.landmark[8].y < hand.landmark[6].y:
                    pen = True

            # =========================
            # DRAW / ERASE
            # =========================
            if pen:
                draw(canvas, prev_x, prev_y, x, y, (255, 255, 255), 8)

            if erase:
                draw(canvas, prev_x, prev_y, x, y, (0, 0, 0), 50)

            prev_x, prev_y = x, y

        # combine
        output = cv2.add(frame, canvas)

        # =========================
        # UI TEXT (IMPORTANT INSTRUCTIONS)
        # =========================
        cv2.putText(output, "✍ Index Finger = Write", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(output, "🧽 Open Palm = Erase", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(output, "ESC = Exit", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        cv2.imshow("AI Air Writing (FIXED)", output)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_air_canvas()