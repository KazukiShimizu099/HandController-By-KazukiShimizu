import time


class FPSCounter:
    def __init__(self):
        self.t0 = time.time()
        self.frames = 0
        self.fps = 0

    def update(self):
        self.frames += 1
        elapsed = time.time() - self.t0
        if elapsed >= 0.5:
            self.fps = self.frames / elapsed
            self.frames = 0
            self.t0 = time.time()
        return self.fps