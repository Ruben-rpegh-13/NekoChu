import pygame
import sys
import os
import time

from config import WIDTH, HEIGHT, FPS, FRAME_WIDTH, FRAME_HEIGHT
from Src.animation import load_sprite_sheet
from Src.entity import Entity
from Src.movement import move_towards

pygame.init()

os.environ["SDL_VIDEO_WINDOW_POS"] = "100,100"
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("NekoChu ⚡")

clock = pygame.time.Clock()

frames = load_sprite_sheet("sprites/pikachu64.png", FRAME_WIDTH, FRAME_HEIGHT)

animations = {
    "walk_right": frames[0],
    "walk_left": frames[1],
    "idle_right": frames[2],
    "idle_left": frames[3],
    "drag_right": frames[2],
    "drag_left": frames[3],
    "sleep_right": frames[2],
    "sleep_left": frames[3],
    "yawn_right": frames[2],
    "yawn_left": frames[3],
}

nekochu = Entity(100, 100, animations)

dragging = False
last_mouse_pos = pygame.mouse.get_pos()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            nekochu.last_mouse_move = time.time()
            if nekochu.state == "sleep":
                nekochu.set_state("idle")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            nekochu.last_mouse_move = time.time()
            if nekochu.state == "sleep":
                nekochu.set_state("idle")

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if nekochu.state == "sleep":
                nekochu.set_state("idle")

    mx, my = pygame.mouse.get_pos()

    if (mx, my) != last_mouse_pos:
        nekochu.last_mouse_move = time.time()
        nekochu.is_sleeping = False
        last_mouse_pos = (mx, my)

    idle_time = time.time() - nekochu.last_mouse_move

    if idle_time > nekochu.sleep_delay:
        nekochu.is_sleeping = True
        nekochu.set_state("sleep")
    elif idle_time > nekochu.yawn_delay:
        nekochu.set_state("yawn")

    if dragging:
        nekochu.x = mx
        nekochu.y = my
        nekochu.set_state("drag")
        nekochu.vx = 0
        nekochu.vy = 0
    elif not nekochu.is_sleeping and idle_time <= nekochu.yawn_delay:
        move_towards(nekochu, mx, my)

    nekochu.update_animation()

    screen.fill((0, 0, 0))
    nekochu.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
