import pygame
import random
import math


class TextBubble:
    def __init__(self, font):
        self.font = font
        self.text = ""
        self.duration = 0
        self.timer = 0
        self.alpha = 255
        self.y_offset = 0

    def show(self, text, duration=2.0):
        self.text = text
        self.duration = duration
        self.timer = 0
        self.alpha = 255
        self.y_offset = 0

    def update(self, dt):
        if self.text:
            self.timer += dt
            self.y_offset = max(0, -10 + self.timer * 20)
            if self.timer >= self.duration * 0.7:
                self.alpha = max(
                    0,
                    255
                    - (self.timer - self.duration * 0.7) / (self.duration * 0.3) * 255,
                )
            if self.timer >= self.duration:
                self.text = ""

    def draw(self, surface, x, y):
        if self.text and self.alpha > 0:
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x, y - 50 - self.y_offset))

            bg_rect = text_rect.inflate(20, 10)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, min(200, self.alpha)))
            pygame.draw.rect(
                bg_surface,
                (100, 100, 100, min(200, self.alpha)),
                bg_surface.get_rect(),
                2,
            )

            text_surface.set_alpha(self.alpha)
            surface.blit(bg_surface, bg_rect)
            surface.blit(text_surface, text_rect)


class LightningEffect:
    def __init__(self, font):
        self.font = font
        self.active = False
        self.timer = 0
        self.duration = 0
        self.message = ""
        self.bolts = []
        self.flash_timer = 0
        self.show_flash = False

    def activate(self, duration, message=""):
        self.active = True
        self.duration = duration
        self.timer = 0
        self.message = message
        self.bolts = []
        self._generate_bolts()

    def deactivate(self):
        self.active = False
        self.bolts = []
        self.show_flash = False

    def is_active(self):
        return self.active

    def _generate_bolts(self):
        self.bolts = []
        for _ in range(3):
            start_x = random.randint(-30, 30)
            points = [(0, start_x)]
            x = 0
            y = start_x
            for _ in range(random.randint(4, 7)):
                x += random.randint(5, 15)
                y += random.randint(-20, 20)
                points.append((x, y))
            self.bolts.append(points)

    def update(self, dt):
        if not self.active:
            return

        self.timer += dt
        self.flash_timer += dt

        if self.flash_timer > 0.08:
            self.flash_timer = 0
            self.show_flash = not self.show_flash
            if self.show_flash:
                self._generate_bolts()

        if self.timer >= self.duration:
            self.deactivate()

    def draw(self, surface, x, y):
        if not self.active:
            return

        center_x = x + 32
        center_y = y

        if self.show_flash:
            for i, bolt in enumerate(self.bolts):
                color = (255, 255, 0) if i == 0 else (255, 200, 0)
                points = [(center_x + px, center_y + 20 + py) for px, py in bolt]
                if len(points) > 1:
                    pygame.draw.lines(surface, color, False, points, 2 + i)

        if self.message:
            text_surface = self.font.render(self.message, True, (255, 255, 0))
            text_rect = text_surface.get_rect(center=(center_x, center_y - 30))
            surface.blit(text_surface, text_rect)
