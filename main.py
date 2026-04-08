"""
NekoChu - Animated Pikachu desktop mascot.
"""

import random
import pygame
import sys
import os

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, SPRITE_SIZE, 
    WINDOW_POSITION, BG_COLOR, ANNOYANCE_DURATION,
    ANNOYANCE_MESSAGES, RAGE_DURATION, RAGE_MESSAGES
)
from src.animation import load_sprite_sheet
from src.entity import Entity
from src.movement import move_towards
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

frames = load_sprite_sheet("sprites/pikachu64.png", SPRITE_SIZE, SPRITE_SIZE)

animations = {
    "walk_right": frames[0],
    "walk_left": frames[1],
    "idle_right": frames[2],
    "idle_left": frames[3],
    "drag_right": frames[2],
    "drag_left": frames[3],
    "sleep_right": frames[2],
    "sleep_left": frames[3],
    "annoyed_right": frames[0],
    "annoyed_left": frames[1],
    "rage_right": frames[0],
    "rage_left": frames[1],
}

nekochu = Entity(100, 100, animations)
dragging = False

screen.fill(BG_COLOR)
pygame.display.update()


def handle_event(event) -> None:
    """Process a single pygame event."""
    global dragging
    
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        sleep_manager.record_activity()
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)
        elif nekochu.state == "annoyed":
            nekochu.set_state("idle")
        elif nekochu.state == "rage":
            nekochu.set_state("idle")
            lightning_effect.deactivate()
    
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos
        
        if nekochu.contains_point(mx, my) and nekochu.state not in ("sleep", "rage"):
            should_rage, message = click_tracker.record_click()
            
            if should_rage:
                nekochu.set_state("rage", RAGE_DURATION)
                rage_msg = random.choice(RAGE_MESSAGES)
                lightning_effect.activate(RAGE_DURATION, rage_msg)
                text_bubble.show(rage_msg, RAGE_DURATION)
            elif message:
                nekochu.set_state("annoyed", ANNOYANCE_DURATION)
                text_bubble.show(message, ANNOYANCE_MESSAGE_DURATION)
            else:
                if nekochu.state == "annoyed":
                    remaining = len(ANNOYANCE_MESSAGES) - click_tracker.message_index
                    if remaining > 0:
                        text_bubble.show(f"¡{remaining} avisos quedan!", 1.0)
        else:
            dragging = True
        
        sleep_manager.record_activity()
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)
    
    elif event.type == pygame.MOUSEBUTTONUP:
        dragging = False
        sleep_manager.record_activity()
    
    elif event.type == pygame.MOUSEMOTION:
        sleep_manager.record_activity()
        if nekochu.state == "sleep":
            sleep_manager.wake_up(nekochu)


def update() -> None:
    """Update entity state and position."""
    global dragging
    
    if nekochu.should_return_to_idle() and nekochu.state == "annoyed":
        nekochu.set_state("idle")
    
    if nekochu.should_return_to_idle() and nekochu.state == "rage":
        nekochu.set_state("idle")
        lightning_effect.deactivate()
    
    if lightning_effect.is_active():
        lightning_effect.update()
    
    if sleep_manager.should_sleep() and nekochu.state not in ("sleep", "rage", "drag", "annoyed"):
        nekochu.set_state("sleep")
    
    mx, my = pygame.mouse.get_pos()
    
    if dragging:
        nekochu.x = mx - SPRITE_SIZE // 2
        nekochu.y = my - SPRITE_SIZE // 2
        nekochu.set_state("drag")
    elif nekochu.state not in ("sleep", "annoyed", "rage"):
        move_towards(nekochu, mx, my)
    
    nekochu.update_animation()


def render() -> None:
    """Draw everything to the screen."""
    screen.fill(BG_COLOR)
    nekochu.draw(screen)
    
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
