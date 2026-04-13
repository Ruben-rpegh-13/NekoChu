"""
NekoChu — mascota de escritorio animada para Windows.

Orden de arranque (crítico):
  1. enable_dpi_awareness()   — antes de cualquier llamada a pygame
  2. check_platform()         — falla rápido si no es Windows
  3. pygame.init()
  4. Crear ventana fullscreen NOFRAME
  5. setup_transparent_window() — sobre el HWND de esa ventana
  6. Bucle principal
"""

import math
import os
import random
import sys
import time

import pygame

# ── Plataforma primero, antes que nada ───────────────────────────────
from src.platform_layer import (
    check_platform,
    enable_dpi_awareness,
    get_screen_size,
    get_taskbar_height,
    refresh_topmost,
    setup_transparent_window,
)

check_platform()
enable_dpi_awareness()

# ── Resto de imports del proyecto ─────────────────────────────────────
from config import (
    FPS,
    SPRITE_SIZE,
    COLORKEY,
    ANNOYANCE_DURATION,
    ANNOYANCE_MESSAGE_DURATION,
    RAGE_DURATION,
    SPEED,
    STOP_DISTANCE,
    FALL_THRESHOLD,
    DUST_OFFSET_X,
    DUST_OFFSET_Y,
    TOPMOST_REFRESH_INTERVAL,
)
from src.animation import load_gif_frames
from src.entity import Entity
from src.sleep import SleepManager
from src.interaction import ClickTracker
from src.effects import TextBubble, LightningEffect

# ── Inicialización de pygame ──────────────────────────────────────────

pygame.init()

SCREEN_W, SCREEN_H = get_screen_size()
TASKBAR_H = get_taskbar_height()
GROUND_Y = SCREEN_H - SPRITE_SIZE - TASKBAR_H

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.NOFRAME)
pygame.display.set_caption("NekoChu")

hwnd = pygame.display.get_wm_info()["window"]
setup_transparent_window(hwnd, COLORKEY)

# ── Subsistemas ───────────────────────────────────────────────────────

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
sleep_manager = SleepManager()
click_tracker = ClickTracker()
text_bubble = TextBubble(font)
lightning = LightningEffect(font)

# ── Carga de sprites ──────────────────────────────────────────────────


def _make_fallback(n: int = 4) -> list:
    return [
        pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA) for _ in range(n)
    ]


def _load_gif(path: str, fallback_n: int = 4) -> list:
    frames = load_gif_frames(path)
    if not frames:
        print(f"[WARN] Sprite no encontrado: {path!r}")
        return _make_fallback(fallback_n)
    return frames


def _load_img(path: str) -> pygame.Surface:
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (SPRITE_SIZE, SPRITE_SIZE))
    except pygame.error:
        print(f"[WARN] Imagen no encontrada: {path!r}")
        return pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)


walk_frames = _load_gif("sprites/pokeapi/pikachu_walk.gif")
idle_frames = _load_gif("sprites/pokeapi/pikachu_crystal.gif", fallback_n=2)
sleep_frames = [_load_img("sprites/wikidex/sleep.png")]
annoyed_frames = [_load_img("sprites/wikidex/angry.png")]


def _flipped(frames: list) -> list:
    return [pygame.transform.flip(f, True, False) for f in frames]


animations = {
    "walk_right": walk_frames,
    "walk_left": _flipped(walk_frames),
    "idle_right": idle_frames,
    "idle_left": _flipped(idle_frames),
    "drag_right": idle_frames,
    "drag_left": _flipped(idle_frames),
    "sleep_right": sleep_frames,
    "sleep_left": _flipped(sleep_frames),
    "annoyed_right": annoyed_frames,
    "annoyed_left": _flipped(annoyed_frames),
    "rage_right": walk_frames,
    "rage_left": _flipped(walk_frames),
    "jump_right": idle_frames,
    "fall_right": idle_frames,
    "dust": _make_fallback(1),
}

# ── Entidad principal ─────────────────────────────────────────────────

nekochu = Entity(100, GROUND_Y, animations)
nekochu.ground_y = GROUND_Y

# ── Estado del bucle ──────────────────────────────────────────────────

dragging = False
previous_mouse_x = pygame.mouse.get_pos()[0]
dust_animation = None
dust_timer = 0.0
_last_topmost = time.time()


# ── Funciones del bucle ───────────────────────────────────────────────


def _is_on_sprite(mx: int, my: int) -> bool:
    """True solo si el cursor está sobre un píxel no transparente del sprite."""
    if not nekochu.contains_point(mx, my):
        return False
    frame = nekochu.get_current_frame()
    lx = mx - int(nekochu.x)
    ly = my - int(nekochu.y)
    lx = max(0, min(lx, frame.get_width() - 1))
    ly = max(0, min(ly, frame.get_height() - 1))
    return frame.get_at((lx, ly)).a > 0


def handle_event(event: pygame.event.Event) -> None:
    global dragging, previous_mouse_x

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_s:
            nekochu.set_state("sleep", ANNOYANCE_DURATION)
        elif event.key == pygame.K_a:
            nekochu.set_state("annoyed", ANNOYANCE_DURATION)
        elif event.key == pygame.K_r:
            nekochu.set_state("rage", RAGE_DURATION)
            lightning.activate(RAGE_DURATION, random.choice(["¡PIKAAAAA!", "⚡⚡⚡"]))

        sleep_manager.record_activity()
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos
        previous_mouse_x = mx

        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)
            sleep_manager.record_activity()
            return

        if _is_on_sprite(mx, my):
            if nekochu.state not in ("rage", "jump", "fall"):
                should_rage, message = click_tracker.record_click()
                if should_rage:
                    nekochu.set_state("rage", RAGE_DURATION)
                    lightning.activate(
                        RAGE_DURATION,
                        random.choice(
                            ["¡PIKAAAAA-CHUUUUU!", "¡THUNDER SHOCK!", "¡RAYO MÁXIMO!"]
                        ),
                    )
                elif message:
                    nekochu.set_state("annoyed", ANNOYANCE_DURATION)
                    text_bubble.show(message, ANNOYANCE_MESSAGE_DURATION)
        else:
            if nekochu.state not in ("rage",):
                dragging = True
                nekochu.start_drag(mx, my)

        sleep_manager.record_activity()

    elif event.type == pygame.MOUSEBUTTONUP:
        if dragging:
            dragging = False
            nekochu.end_drag()
        sleep_manager.record_activity()

    elif event.type == pygame.MOUSEMOTION:
        sleep_manager.record_activity()
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)


def update(dt: float) -> None:
    global dragging, previous_mouse_x, dust_timer, dust_animation, _last_topmost

    mx, my = pygame.mouse.get_pos()
    mouse_moving = abs(mx - previous_mouse_x) > FALL_THRESHOLD

    now = time.time()
    if now - _last_topmost >= TOPMOST_REFRESH_INTERVAL:
        refresh_topmost(hwnd)
        _last_topmost = now

    if nekochu.should_return_to_idle(dt) and nekochu.state in ("annoyed", "rage"):
        nekochu.set_state("idle")
        lightning.deactivate()

    if lightning.is_active():
        lightning.update(dt)
    else:
        text_bubble.update(dt)

    if sleep_manager.should_sleep() and nekochu.state not in (
        "sleep",
        "rage",
        "drag",
        "annoyed",
        "jump",
        "fall",
    ):
        nekochu.set_state("sleep")

    if nekochu.state == "sleep" and mouse_moving:
        sleep_manager.wake_up(nekochu)

    if dragging:
        nekochu.x = mx - nekochu.drag_offset_x
        nekochu.y = my - nekochu.drag_offset_y
        nekochu.set_state("drag")
        nekochu.vx = 0
        nekochu.vy = 0
        nekochu.x = max(0, min(nekochu.x, SCREEN_W - SPRITE_SIZE))
        nekochu.y = max(0, min(nekochu.y, SCREEN_H - SPRITE_SIZE))
    else:
        nekochu.apply_physics(dt)

        if nekochu.falling_after_drag and not nekochu.on_ground:
            nekochu.set_state("jump" if nekochu.vy < 0 else "fall")
        elif nekochu.state not in ("annoyed", "rage", "sleep"):
            target_x = mx - SPRITE_SIZE // 2
            target_y = GROUND_Y

            dx = target_x - nekochu.x
            dy = target_y - nekochu.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > STOP_DISTANCE:
                nekochu.set_state("walk")
                nekochu.direction = "right" if dx > 0 else "left"
                factor = SPEED / distance
                nekochu.x += dx * factor
                nekochu.y += dy * factor
            else:
                if nekochu.state == "walk":
                    nekochu.set_state("idle")

        nekochu.x = max(0, min(nekochu.x, SCREEN_W - SPRITE_SIZE))

    if nekochu.dust_active:
        if dust_animation is None:
            dust_animation = 0
            dust_timer = 0.0
        dust_timer += dt
        if dust_timer > 0.24:
            nekochu.dust_active = False
            dust_animation = None

    nekochu.update_animation()
    previous_mouse_x = mx


def render() -> None:
    screen.fill(COLORKEY)

    nekochu.draw(screen)

    if nekochu.dust_active and dust_animation is not None:
        dust_frames = animations["dust"]
        dust_frame_idx = min(int(dust_timer / 0.06), len(dust_frames) - 1)
        dust_surf = dust_frames[dust_frame_idx]
        dx = int(nekochu.x + SPRITE_SIZE // 2 - 32 + DUST_OFFSET_X)
        dy = int(GROUND_Y + SPRITE_SIZE - 32 + DUST_OFFSET_Y)
        screen.blit(dust_surf, (dx, dy))

    if lightning.is_active():
        lightning.draw(screen, int(nekochu.x), int(nekochu.y))
    else:
        text_bubble.draw(screen, int(nekochu.x + SPRITE_SIZE // 2), int(nekochu.y))

    pygame.display.update()


def main() -> None:
    while True:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            handle_event(event)

        update(dt)
        render()


if __name__ == "__main__":
    main()
