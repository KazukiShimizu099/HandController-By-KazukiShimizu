"""Cross-platform low-latency mouse controller using pynput."""
from pynput.mouse import Controller, Button
from screeninfo import get_monitors
import numpy as np
import config
from core.smoothing import OneEuroFilter


class MouseController:
    def __init__(self):
        self.mouse = Controller()
        m = get_monitors()[0]
        self.screen_w, self.screen_h = m.width, m.height

        self.fx = OneEuroFilter(freq=60, mincutoff=config.MIN_CUTOFF,
                                 beta=config.BETA, dcutoff=config.D_CUTOFF)
        self.fy = OneEuroFilter(freq=60, mincutoff=config.MIN_CUTOFF,
                                 beta=config.BETA, dcutoff=config.D_CUTOFF)

        self.dragging = False
        self.prev_scroll = None

    def _map_to_screen(self, nx, ny):
        """Map normalized [0..1] coordinates to screen with frame reduction."""
        rx, ry = config.FRAME_REDUCTION_X, config.FRAME_REDUCTION_Y
        # Clamp normalized coords to active region
        nx = (nx - rx) / (1 - 2 * rx)
        ny = (ny - ry) / (1 - 2 * ry)
        nx = np.clip(nx, 0.0, 1.0)
        ny = np.clip(ny, 0.0, 1.0)
        return int(nx * self.screen_w), int(ny * self.screen_h)

    def move(self, nx, ny):
        sx, sy = self._map_to_screen(nx, ny)
        sx = self.fx(sx)
        sy = self.fy(sy)
        self.mouse.position = (int(sx), int(sy))

    def left_click(self):
        self.mouse.click(Button.left, 1)

    def right_click(self):
        self.mouse.click(Button.right, 1)

    def start_drag(self, nx, ny):
        if not self.dragging:
            self.move(nx, ny)
            self.mouse.press(Button.left)
            self.dragging = True

    def drag_to(self, nx, ny):
        self.move(nx, ny)

    def end_drag(self):
        if self.dragging:
            self.mouse.release(Button.left)
            self.dragging = False

    def scroll(self, current_y):
        if self.prev_scroll is None:
            self.prev_scroll = current_y
            return
        delta = (self.prev_scroll - current_y) * 80  # sensitivity
        if abs(delta) > 0.5:
            self.mouse.scroll(0, int(delta))
        self.prev_scroll = current_y

    def reset_scroll(self):
        self.prev_scroll = None