"""
Configuration constants for NekoChu.
"""

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

SPRITE_SIZE = 64
FRAME_WIDTH = 64
FRAME_HEIGHT = 64

SPEED = 2.5
STOP_DISTANCE = 10

ANIMATION_DELAYS = {
    "idle": 0.3,
    "walk": 0.1,
    "drag": 0.5,
    "sleep": 0.5,
    "annoyed": 0.15,
    "rage": 0.08,
}

SLEEP_TIMEOUT = 10.0

WINDOW_POSITION = (100, 100)

ANNOYANCE_CLICKS = 5
ANNOYANCE_DURATION = 3.0
ANNOYANCE_MESSAGE_DURATION = 0.8
CLICK_THRESHOLD = 0.5
ANNOYANCE_RESET_TIME = 2.0

RAGE_DURATION = 4.0
RAGE_COOLDOWN = 15.0

ANNOYANCE_MESSAGES = [
    "¡Pii!",
    "¡Pika!",
    "¡Pi-ka!",
    "¡PIKA-CHU!",
    "¡Ya basta!",
    "¡No más!",
    "...",
    "¡Última advertencia!",
]

RAGE_MESSAGES = [
    "¡PIKAAAAA-CHUUUUU!",
    "¡THUNDER SHOCK!",
    "¡RAYO MÁXIMO!",
]

BG_COLOR = (0, 0, 0)
