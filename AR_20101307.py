import cv2
import numpy as np
import mediapipe as mp

dog_img = cv2.imread("dog.png", cv2.IMREAD_UNCHANGED)
dog_img = cv2.resize(dog_img, (200, 200))
cat_img = cv2.imread("cat.png", cv2.IMREAD_UNCHANGED)
cat_img = cv2.resize(cat_img, (200, 200))

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

GESTURE_HOLD_FRAMES = 5
gesture_state = None
gesture_counter = 0
confirmed_gesture = None

def count_extended_fingers(landmarks):
    tips = [8, 12, 16, 20]
    bases = [5, 9, 13, 17]
    return sum(1 for tip, base in zip(tips, bases) if landmarks[tip].y < landmarks[base].y - 0.02)

def overlay_image(bg, fg, x, y):
    h, w = fg.shape[:2]
    x, y = int(x - w/2), int(y - h/2)
    if x < 0 or y < 0 or x + w > bg.shape[1] or y + h > bg.shape[0]: return bg
    alpha = fg[:, :, 3] / 255.0
    for c in range(3):
        bg[y:y+h, x:x+w, c] = (1 - alpha) * bg[y:y+h, x:x+w, c] + alpha * fg[:, :, c]
    return bg

def draw_fixed_cube(frame, cx, cy, size=100):
    offset = int(size / 2)
    front = np.array([
        [cx - offset, cy - offset],
        [cx + offset, cy - offset],
        [cx + offset, cy + offset],
        [cx - offset, cy + offset]
    ], dtype=np.int32)

    depth = int(size * 0.5)
    back = front - [depth, depth]

    for face in [front, back]:
        cv2.polylines(frame, [face], isClosed=True, color=(0, 255, 0), thickness=2)

    for f, b in zip(front, back):
        cv2.line(frame, tuple(f), tuple(b), (0, 255, 0), 2)

    return frame

cap = cv2.VideoCapture("hand.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture_now = "none"
    lm = []
    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        count = count_extended_fingers(lm)
        if count >= 4:
            gesture_now = "cube"
        elif count == 2:
            gesture_now = "dog"
        elif count == 1:
            gesture_now = "cat"

    if gesture_now == gesture_state:
        gesture_counter += 1
    else:
        gesture_state = gesture_now
        gesture_counter = 1

    if gesture_counter >= GESTURE_HOLD_FRAMES:
        confirmed_gesture = gesture_state

    if confirmed_gesture == "cube" and lm:
        cx, cy = int(lm[9].x * w) + 20, int(lm[9].y * h)
        frame = draw_fixed_cube(frame, cx, cy)

    elif confirmed_gesture == "dog" and lm:
        cx, cy = int(lm[9].x * w), int(lm[9].y * h)
        frame = overlay_image(frame, dog_img, cx, cy)
        cv2.putText(frame, "DOG!", (cx - 50, cy + 130), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

    elif confirmed_gesture == "cat" and lm:
        cx, cy = int(lm[9].x * w), int(lm[9].y * h)
        frame = overlay_image(frame, cat_img, cx, cy)
        cv2.putText(frame, "CAT!", (cx - 50, cy + 130), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

    out.write(frame)

cap.release()
out.release()
