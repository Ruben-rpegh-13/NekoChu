"""
Configuration constants for NekoChu.
"""

# ── Ventana ────────────────────────────────────────────────────────

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_POSITION = (100, 100)

FPS = 60

# ── Sprite y animación ────────────────────────────────────────────────

SPRITE_SIZE = 64
FRAME_WIDTH = 64
FRAME_HEIGHT = 64

ANIMATION_DELAYS = {
    "idle": 0.30,
    "walk": 0.08,
    "drag": 0.15,
    "sleep": 0.40,
    "yawn": 0.12,
    "annoyed": 0.07,
    "rage": 0.05,
    "jump": 0.10,
    "fall": 0.12,
    "dust": 0.06,
}

# ── Movimiento ──────────────────────────────────────────────────────��─

SPEED = 6
STOP_DISTANCE = 10
WALK_THRESHOLD = 35

GRAVITY = 1200
JUMP_STRENGTH = -520
FALL_THRESHOLD = 10

DRAG_THRESHOLD = 5

DUST_OFFSET_X = 0
DUST_OFFSET_Y = 28

# ── Sistema de sueño ──────────────────────────────────────────────────

SLEEP_TIMEOUT = 10.0

# ── Sistema de enfado ─────────────────────────────────────────────────

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

# ── Render ────────────────────────────────────────────────────────────

COLORKEY = (1, 1, 1)

BUBBLE_BG_COLOR = (30, 30, 30)
BUBBLE_TEXT_COLOR = (255, 255, 255)

# ── Mantenimiento always-on-top ────────────────────────────────────────

TOPMOST_REFRESH_INTERVAL = 5.0

# ── Render colors ──────────────────────────────────────────────────────────

BG_COLOR = (0, 0, 0)
GROUND_COLOR = (34, 139, 34)
GROUND_HEIGHT = 80
