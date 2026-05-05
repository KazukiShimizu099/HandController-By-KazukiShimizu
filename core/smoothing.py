"""
One Euro Filter - the gold standard for real-time pointer smoothing.
Reference: Casiez et al. CHI 2012.
"""
import math
import time


class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.y = None
        self.s = None

    def __call__(self, value, alpha=None):
        if alpha is not None:
            self.alpha = alpha
        if self.y is None:
            s = value
        else:
            s = self.alpha * value + (1.0 - self.alpha) * self.s
        self.y = value
        self.s = s
        return s


class OneEuroFilter:
    def __init__(self, freq=60.0, mincutoff=1.0, beta=0.0, dcutoff=1.0):
        self.freq = freq
        self.mincutoff = mincutoff
        self.beta = beta
        self.dcutoff = dcutoff
        self.x_filter = LowPassFilter(self._alpha(mincutoff))
        self.dx_filter = LowPassFilter(self._alpha(dcutoff))
        self.last_time = None

    def _alpha(self, cutoff):
        tau = 1.0 / (2 * math.pi * cutoff)
        te = 1.0 / self.freq
        return 1.0 / (1.0 + tau / te)

    def __call__(self, x, t=None):
        if t is None:
            t = time.time()
        if self.last_time is not None and t > self.last_time:
            self.freq = 1.0 / (t - self.last_time)
        self.last_time = t

        prev = self.x_filter.y if self.x_filter.y is not None else x
        dx = (x - prev) * self.freq
        edx = self.dx_filter(dx, self._alpha(self.dcutoff))
        cutoff = self.mincutoff + self.beta * abs(edx)
        return self.x_filter(x, self._alpha(cutoff))