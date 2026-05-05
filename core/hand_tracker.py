"""MediaPipe-based hand tracker with optimized inference."""
import cv2
import mediapipe as mp
import config


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_HANDS,
            model_complexity=1,
            min_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles

    def process(self, frame_bgr):
        # Convert to RGB once - MediaPipe needs RGB
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self.hands.process(rgb)
        return results

    def draw(self, frame, results):
        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, lm, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_styles.get_default_hand_landmarks_style(),
                    self.mp_styles.get_default_hand_connections_style(),
                )

    def close(self):
        self.hands.close()