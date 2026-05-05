import cv2
import config


def draw_hud(frame, fps, action_type, fingers):
    h, w = frame.shape[:2]
    # Active region rectangle
    rx = int(w * config.FRAME_REDUCTION_X)
    ry = int(h * config.FRAME_REDUCTION_Y)
    cv2.rectangle(frame, (rx, ry), (w - rx, h - ry), (0, 255, 0), 2)

    # HUD text
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Action: {action_type}", (10, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    if fingers:
        cv2.putText(frame, f"Fingers: {fingers}", (10, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
    cv2.putText(frame, "Press 'q' to quit | 'p' to pause",
                (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    