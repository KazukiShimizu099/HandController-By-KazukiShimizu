"""
Gesture Map:
  • Index finger up only         -> Move cursor
  • Pinch (thumb + index)        -> Left click
  • Pinch (thumb + middle)       -> Right click
  • Hold pinch + move            -> Drag & drop
  • Index + Middle up + move up/down -> Scroll
  • Open palm (5 fingers)        -> Idle / pause
  • Fist                         -> Disable mouse
"""
import math
import time
import config


# MediaPipe landmark indices
WRIST = 0
THUMB_TIP, THUMB_IP = 4, 3
INDEX_TIP, INDEX_PIP, INDEX_MCP = 8, 6, 5
MIDDLE_TIP, MIDDLE_PIP = 12, 10
RING_TIP, RING_PIP = 16, 14
PINKY_TIP, PINKY_PIP = 20, 18


def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def fingers_up(landmarks, handedness="Right"):
    """Returns [thumb, index, middle, ring, pinky] booleans."""
    lm = landmarks.landmark
    fingers = []

    # Thumb (horizontal check)
    if handedness == "Right":
        fingers.append(lm[THUMB_TIP].x < lm[THUMB_IP].x)
    else:
        fingers.append(lm[THUMB_TIP].x > lm[THUMB_IP].x)

    # Other fingers (vertical: tip above pip)
    for tip, pip in [(INDEX_TIP, INDEX_PIP), (MIDDLE_TIP, MIDDLE_PIP),
                     (RING_TIP, RING_PIP), (PINKY_TIP, PINKY_PIP)]:
        fingers.append(lm[tip].y < lm[pip].y)
    return fingers


class GestureRecognizer:
    def __init__(self):
        self.last_click_time = 0
        self.pinch_frames = 0
        self.is_dragging = False
        self.scroll_frames = 0
        self.prev_scroll_y = None

    def detect(self, landmarks, handedness="Right"):
        """Returns dict of action + cursor anchor point."""
        lm = landmarks.landmark
        fingers = fingers_up(landmarks, handedness)

        # Cursor anchor = index fingertip
        cursor_pt = (lm[INDEX_TIP].x, lm[INDEX_TIP].y)

        action = {"type": "idle", "cursor": cursor_pt, "fingers": fingers}

        # FIST -> disable
        if not any(fingers):
            action["type"] = "disable"
            return action

        # OPEN PALM -> pause
        if all(fingers):
            action["type"] = "pause"
            return action

        # SCROLL: index + middle up, others down
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            action["type"] = "scroll"
            action["scroll_y"] = lm[INDEX_TIP].y
            return action

        # PINCH detection
        pinch_index = distance(lm[THUMB_TIP], lm[INDEX_TIP])
        pinch_middle = distance(lm[THUMB_TIP], lm[MIDDLE_TIP])

        now = time.time() * 1000

        # RIGHT CLICK
        if pinch_middle < config.RIGHT_CLICK_THRESHOLD and fingers[1]:
            if now - self.last_click_time > config.CLICK_COOLDOWN_MS:
                self.last_click_time = now
                action["type"] = "right_click"
                return action

        # LEFT CLICK / DRAG
        if pinch_index < config.CLICK_THRESHOLD:
            self.pinch_frames += 1
            if self.pinch_frames >= config.DRAG_HOLD_FRAMES:
                action["type"] = "drag"
                self.is_dragging = True
            else:
                action["type"] = "pinch"
            return action
        else:
            if self.is_dragging:
                action["type"] = "drop"
                self.is_dragging = False
                self.pinch_frames = 0
                return action
            if 0 < self.pinch_frames < config.DRAG_HOLD_FRAMES:
                if now - self.last_click_time > config.CLICK_COOLDOWN_MS:
                    self.last_click_time = now
                    action["type"] = "left_click"
            self.pinch_frames = 0

        # MOVE: only index up
        if fingers[1] and not fingers[2]:
            action["type"] = "move"

        return action