"""Central configuration - tweak these to your liking."""

# Camera
CAM_INDEX = 0
CAM_WIDTH = 640
CAM_HEIGHT = 480
CAM_FPS = 60

# Hand detection
DETECTION_CONFIDENCE = 0.75
TRACKING_CONFIDENCE = 0.6
MAX_HANDS = 1

# Mouse control region (frame area mapped to whole screen)
# Smaller = more sensitive. Values are ratios of frame.
FRAME_REDUCTION_X = 0.15   # 15% margin on left/right
FRAME_REDUCTION_Y = 0.15

# Smoothing (One Euro Filter)
MIN_CUTOFF = 1.0           # lower = smoother but more lag
BETA = 0.05                # higher = faster response on quick moves
D_CUTOFF = 1.0

# Gesture thresholds (normalized distance between landmarks)
CLICK_THRESHOLD = 0.04     # thumb-index pinch for left click
RIGHT_CLICK_THRESHOLD = 0.045  # thumb-middle pinch
DRAG_HOLD_FRAMES = 8       # frames to hold pinch before drag starts
SCROLL_ACTIVE_FRAMES = 5

# Click cooldown (prevents accidental double clicks)
CLICK_COOLDOWN_MS = 300

# UI
SHOW_PREVIEW = True
SHOW_LANDMARKS = True
MIRROR_CAMERA = True