"""
NekoChu - Animated Pikachu desktop mascot with physics.
"""

import random
import pygame
import sys
import os

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    SPRITE_SIZE,
    WINDOW_POSITION,
    BG_COLOR,
    GROUND_COLOR,
    GROUND_HEIGHT,
    ANNOYANCE_DURATION,
    ANNOYANCE_MESSAGE_DURATION,
    ANNOYANCE_MESSAGES,
    RAGE_DURATION,
    GRAVITY,
    JUMP_STRENGTH,
    FALL_THRESHOLD,
    WALK_THRESHOLD,
    DUST_OFFSET_X,
    DUST_OFFSET_Y,
)
from src.animation import load_sprite_sheet, load_gif_frames
from src.entity import Entity
from src.sleep import SleepManager
from src.interaction import ClickTracker
from src.effects import TextBubble, LightningEffect

pygame.init()

os.environ["SDL_VIDEO_WINDOW_POS"] = f"{WINDOW_POSITION[0]},{WINDOW_POSITION[1]}"
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("NekoChu ⚡")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
sleep_manager = SleepManager()
click_tracker = ClickTracker()
text_bubble = TextBubble(font)
lightning_effect = LightningEffect(font)

walk_frames = load_gif_frames("sprites/pokeapi/pikachu_walk.gif")
idle_frames = load_gif_frames("sprites/pokeapi/pikachu_crystal.gif")


def make_fallback(rows=1, cols=4):
    return [
        pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
        for _ in range(rows * cols)
    ]


if not walk_frames:
    walk_frames = make_fallback(1, 4)
if not idle_frames:
    idle_frames = make_fallback(1, 2)

animations = {
    "walk_right": walk_frames,
    "walk_left": [pygame.transform.flip(f, True, False) for f in walk_frames],
    "idle_right": idle_frames,
    "idle_left": [pygame.transform.flip(f, True, False) for f in idle_frames],
    "drag_right": idle_frames,
    "drag_left": [pygame.transform.flip(f, True, False) for f in idle_frames],
    "sleep_right": idle_frames[:1] if idle_frames else make_fallback(1, 1),
    "sleep_left": idle_frames[:1] if idle_frames else make_fallback(1, 1),
    "annoyed_right": idle_frames,
    "annoyed_left": [pygame.transform.flip(f, True, False) for f in idle_frames],
    "rage_right": walk_frames,
    "rage_left": [pygame.transform.flip(f, True, False) for f in walk_frames],
    "jump_right": idle_frames,
    "fall_right": idle_frames,
    "dust": make_fallback(1, 1),
}

ground_y = WINDOW_HEIGHT - SPRITE_SIZE - GROUND_HEIGHT
nekochu = Entity(100, ground_y, animations)
nekochu.ground_y = ground_y

dragging = False
previous_mouse_x = pygame.mouse.get_pos()[0]
dust_animation = None
dust_timer = 0

screen.fill(BG_COLOR)
pygame.display.update()


def handle_event(event) -> None:
    """Process a single pygame event."""
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
            lightning_effect.activate(
                RAGE_DURATION, random.choice(["¡PIKAAAAA!", "¡THUNDER!", "⚡⚡⚡"])
            )

        sleep_manager.record_activity()
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)
        elif nekochu.state in ("annoyed", "rage"):
            nekochu.set_state("idle")
            lightning_effect.deactivate()

    elif event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos
        previous_mouse_x = mx

        if nekochu.contains_point(mx, my) and nekochu.state not in (
            "sleep",
            "rage",
            "jump",
            "fall",
        ):
            should_rage, message = click_tracker.record_click()

            if should_rage:
                nekochu.set_state("rage", RAGE_DURATION)
                lightning_effect.activate(
                    RAGE_DURATION,
                    random.choice(
                        ["¡PIKAAAAA-CHUUUUU!", "¡THUNDER SHOCK!", "¡RAYO MÁXIMO!"]
                    ),
                )
            elif message:
                nekochu.set_state("annoyed", ANNOYANCE_DURATION)
                text_bubble.show(message, ANNOYANCE_MESSAGE_DURATION)
        else:
            dragging = True
            nekochu.start_drag(mx, my)

        sleep_manager.record_activity()
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)

    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False
        nekochu.end_drag()
        sleep_manager.record_activity()

    elif event.type == pygame.MOUSEMOTION:
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)


def update() -> None:
    """Update entity state and position."""
    global dragging, previous_mouse_x, dust_timer, dust_animation

    mx, my = pygame.mouse.get_pos()
    mouse_x = mx
    mouse_moving = abs(mouse_x - previous_mouse_x) > FALL_THRESHOLD

    if nekochu.should_return_to_idle() and nekochu.state in ("annoyed", "rage"):
        nekochu.set_state("idle")
        lightning_effect.deactivate()

    if lightning_effect.is_active():
        lightning_effect.update(1 / FPS)
    else:
        text_bubble.update(1 / FPS)

    if sleep_manager.should_sleep() and nekochu.state not in (
        "sleep",
        "rage",
        "drag",
        "annoyed",
        "jump",
        "fall",
    ):
        nekochu.set_state("sleep")

    if nekochu.state in ("sleep_right", "sleep_left") and mouse_moving:
        nekochu.set_state("idle")

    if dragging:
        nekochu.x = mx - nekochu.drag_offset_x
        nekochu.y = my - nekochu.drag_offset_y
        nekochu.set_state("drag")
        nekochu.vx = 0
        nekochu.vy = 0
    else:
        nekochu.apply_physics(1 / FPS)

        if nekochu.falling_after_drag and not nekochu.on_ground:
            if nekochu.vy < 0:
                nekochu.set_state("jump")
            elif nekochu.vy > FALL_THRESHOLD:
                nekochu.set_state("fall")
        else:
            from config import SPEED, STOP_DISTANCE
            import math

            target_x = mx - SPRITE_SIZE // 2
            target_y = my - SPRITE_SIZE // 2

            dx = target_x - nekochu.x
            dy = target_y - nekochu.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > STOP_DISTANCE:
                nekochu.set_state("walk")
                nekochu.direction = "right" if dx > 0 else "left"

                dx_norm = dx / distance if distance > 0 else 0
                dy_norm = dy / distance if distance > 0 else 0

                nekochu.x += dx_norm * SPEED
                nekochu.y += dy_norm * SPEED
            else:
                if nekochu.state == "walk":
                    nekochu.set_state("idle")

    if nekochu.dust_active:
        if dust_animation is None:
            dust_animation = 0
            dust_timer = 0
        dust_timer += 1 / FPS
        if dust_timer > 0.24:
            nekochu.dust_active = False
            dust_animation = None

    nekochu.update_animation()
    previous_mouse_x = mouse_x


def render() -> None:
    """Draw everything to the screen."""
    screen.fill(BG_COLOR)

    pygame.draw.rect(
        screen, GROUND_COLOR, (0, ground_y + SPRITE_SIZE, WINDOW_WIDTH, GROUND_HEIGHT)
    )

    nekochu.draw(screen)

    if nekochu.dust_active and dust_animation is not None:
        dust_frames = animations["dust"]
        dust_frame_index = min(int(dust_timer / 0.06), len(dust_frames) - 1)
        dust_frame = dust_frames[dust_frame_index]
        dust_x = int(nekochu.x + SPRITE_SIZE // 2 - 32 + DUST_OFFSET_X)
        dust_y = int(ground_y + SPRITE_SIZE - 32 + DUST_OFFSET_Y)
        screen.blit(dust_frame, (dust_x, dust_y))

    if lightning_effect.is_active():
        lightning_effect.draw(screen, int(nekochu.x), int(nekochu.y))
    else:
        text_bubble.draw(screen, int(nekochu.x + SPRITE_SIZE // 2), int(nekochu.y))

    pygame.display.update()


def main() -> None:
    """Main game loop."""
    while True:
        for event in pygame.event.get():
            handle_event(event)

        update()
        render()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
