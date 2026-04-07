import pygame
import sys
import os

from config import WIDTH, HEIGHT, FPS, FRAME_WIDTH, FRAME_HEIGHT
from animation import load_sprite_sheet
from entity import Entity
from movement import move_towards

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("NekoChu ⚡")

clock = pygame.time.Clock()

frames = load_sprite_sheet("sprites/pikachu64.png", FRAME_WIDTH, FRAME_HEIGHT)

animations = {
    "walk_right": frames[0],
    "walk_left": frames[1],
    "idle_right": frames[2],
    "idle_left": frames[3],
}

nekochu = Entity(100, 100, animations)

# Drag & drop
dragging = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    mx, my = pygame.mouse.get_pos()

    if dragging:
        nekochu.x = mx
        nekochu.y = my
        nekochu.set_state("idle")
    else:
        move_towards(nekochu, mx, my)

    nekochu.update_animation()

    screen.fill((0,0,0))
    nekochu.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
