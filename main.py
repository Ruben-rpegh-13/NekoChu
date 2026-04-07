import pygame
import sys
import os

from config import WIDTH, HEIGHT, FPS, FRAME_WIDTH, FRAME_HEIGHT
from src.animation import load_sprite_sheet
from src.entity import Entity
from src.movement import move_towards

pygame.init()

# ---------------------------
# Configuración de la ventana
# ---------------------------
os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"  # posición inicial
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)  # sin bordes
pygame.display.set_caption("NekoChu ⚡")

# Fondo transparente (Windows)
screen.set_alpha(None)
screen.fill((0,0,0))
pygame.display.update()

# Always-on-top (Windows)
try:
    import ctypes
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
except:
    print("Always-on-top no soportado en este SO")

clock = pygame.time.Clock()

# ---------------------------
# Cargar sprite sheet de 64x64
# ---------------------------
frames = load_sprite_sheet("sprites/pikachu64.png", FRAME_WIDTH, FRAME_HEIGHT)

animations = {
    "walk_right": frames[0],
    "walk_left": frames[1],
    "idle_right": frames[2],
    "idle_left": frames[3],
}

# Crear NekoChu
nekoshu = Entity(100, 100, animations)

# ---------------------------
# Loop principal
# ---------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mx, my = pygame.mouse.get_pos()

    move_towards(nekoshu, mx, my)
    nekoshu.update_animation()

    screen.fill((0,0,0,0))  # transparente
    nekoshu.draw(screen)

    pygame.display.update()
    clock.tick(FPS)