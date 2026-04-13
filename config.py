"""
Configuración centralizada de NekoChu.
Las dimensiones de pantalla se resuelven en tiempo de ejecución
a través de platform_layer — no hay valores fijos de ventana.
"""

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

# ── Movimiento ────────────────────────────────────────────────────────

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

# Color usado como fondo transparente.
# CRÍTICO: debe coincidir con lo que se pasa a setup_transparent_window().
# No usar (0,0,0) negro puro — muchos sprites lo tienen en sus bordes.
# (1,1,1) es casi negro, invisible en sprites, y no colisiona con píxeles reales.
COLORKEY = (1, 1, 1)

# Color de fondo de la burbuja de texto
BUBBLE_BG_COLOR = (30, 30, 30)
BUBBLE_TEXT_COLOR = (255, 255, 255)

# ── Mantenimiento always-on-top ────────────────────────────────────────

# Cada cuántos segundos se re-aplica HWND_TOPMOST para resistir eventos
# del sistema (UAC, menú inicio, apps fullscreen) que bajan la ventana.
TOPMOST_REFRESH_INTERVAL = 5.0

# ── FPS ────────────────────────────────────────────────────────────────

FPS = 60
