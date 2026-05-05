"""
Advanced Hand Mouse Controller
Run:   python main.py
Quit:  press 'q'
Pause: press 'p'
"""
import cv2
import config
from core.hand_tracker import HandTracker
from core.gesture_recognizer import GestureRecognizer
from core.mouse_controller import MouseController
from utils.fps_counter import FPSCounter
from utils.visualizer import draw_hud


def main():
    cap = cv2.VideoCapture(config.CAM_INDEX, cv2.CAP_DSHOW)  # DSHOW = fast on Windows
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.CAM_FPS)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # reduce lag

    tracker = HandTracker()
    recognizer = GestureRecognizer()
    mouse = MouseController()
    fps = FPSCounter()

    paused = False
    print("[INFO] Hand Mouse Controller started. Show your hand to the camera.")

    while True:
        ok, frame = cap.read()
        if not ok:
            continue
        if config.MIRROR_CAMERA:
            frame = cv2.flip(frame, 1)

        results = tracker.process(frame)
        action_type = "no_hand"
        fingers = []

        if results.multi_hand_landmarks and not paused:
            handedness = "Right"
            if results.multi_handedness:
                handedness = results.multi_handedness[0].classification[0].label

            lms = results.multi_hand_landmarks[0]
            action = recognizer.detect(lms, handedness)
            action_type = action["type"]
            fingers = action.get("fingers", [])
            nx, ny = action["cursor"]

            if action_type == "move":
                mouse.end_drag()
                mouse.reset_scroll()
                mouse.move(nx, ny)

            elif action_type == "pinch":
                mouse.move(nx, ny)

            elif action_type == "left_click":
                mouse.left_click()

            elif action_type == "right_click":
                mouse.right_click()

            elif action_type == "drag":
                mouse.start_drag(nx, ny)
                mouse.drag_to(nx, ny)

            elif action_type == "drop":
                mouse.end_drag()

            elif action_type == "scroll":
                mouse.end_drag()
                mouse.scroll(action["scroll_y"])

            elif action_type in ("pause", "disable", "idle"):
                mouse.end_drag()
                mouse.reset_scroll()

            if config.SHOW_LANDMARKS:
                tracker.draw(frame, results)

        if config.SHOW_PREVIEW:
            current_fps = fps.update()
            draw_hud(frame, current_fps, action_type, fingers)
            cv2.imshow("Hand Mouse Controller", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('p'):
            paused = not paused
            print(f"[INFO] {'Paused' if paused else 'Resumed'}")

    cap.release()
    cv2.destroyAllWindows()
    tracker.close()


if __name__ == "__main__":
    main()