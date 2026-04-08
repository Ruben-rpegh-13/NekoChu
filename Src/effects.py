"""
Performance optimizations for sprite rendering.
"""

import random
import math
import pygame


class SpriteCache:
    """Cache for pre-processed sprites."""
    
    def __init__(self):
        self._cache: dict[str, pygame.Surface] = {}
    
    def get(self, key: str, loader) -> pygame.Surface:
        if key not in self._cache:
            self._cache[key] = loader()
        return self._cache[key]
    
    def clear(self) -> None:
        self._cache.clear()


class TextBubble:
    """Renderable text bubble."""
    
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.text = ""
        self.surface: pygame.Surface | None = None
        self.lifetime = 0.0
        self.start_time = 0.0
    
    def show(self, text: str, duration: float = 2.0) -> None:
        self.text = text
        self.surface = self.font.render(text, True, (50, 50, 50), (255, 255, 255))
        padding = 8
        self.surface = pygame.Surface(
            (self.surface.get_width() + padding * 2, self.surface.get_height() + padding * 2),
            pygame.SRCALPHA
        )
        pygame.draw.ellipse(self.surface, (255, 255, 255, 230), self.surface.get_rect(), 0)
        inner = self.surface.copy()
        inner.set_alpha(230)
        pygame.draw.ellipse(inner, (255, 255, 255, 255), inner.get_rect(), 0)
        self.surface.blit(inner, (0, 0))
        text_surf = self.font.render(text, True, (50, 50, 50))
        self.surface.blit(text_surf, (padding, padding))
        self.lifetime = duration
        self.start_time = pygame.time.get_ticks() / 1000.0
    
    def is_visible(self) -> bool:
        if not self.surface:
            return False
        elapsed = pygame.time.get_ticks() / 1000.0 - self.start_time
        return elapsed < self.lifetime
    
    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        if self.surface and self.is_visible():
            screen.blit(self.surface, (x - self.surface.get_width() // 2, y - self.surface.get_height() - 20))


class LightningEffect:
    """Animated lightning bolt effect around the entity."""
    
    def __init__(self, font=None):
        self.active = False
        self.lifetime = 0.0
        self.start_time = 0.0
        self.frame_index = 0
        self.bolts: list[dict] = []
        self.font = font
        self.text = ""
        self.text_surface: pygame.Surface | None = None
    
    def activate(self, duration: float = 4.0, message: str = "") -> None:
        self.active = True
        self.lifetime = duration
        self.start_time = pygame.time.get_ticks() / 1000.0
        self.frame_index = 0
        self.text = message
        self._generate_bolts()
    
    def _generate_bolts(self) -> None:
        self.bolts = []
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, 100)
            self.bolts.append({
                "angle": angle,
                "distance": distance,
                "size": random.randint(20, 40),
                "speed": random.uniform(0.5, 1.5),
                "phase": random.uniform(0, 2 * math.pi),
            })
    
    def is_active(self) -> bool:
        if not self.active:
            return False
        elapsed = pygame.time.get_ticks() / 1000.0 - self.start_time
        return elapsed < self.lifetime
    
    def update(self) -> None:
        if not self.is_active():
            return
        self.frame_index += 1
    
    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        if not self.is_active():
            return
        
        elapsed = pygame.time.get_ticks() / 1000.0 - self.start_time
        intensity = min(1.0, elapsed / 0.5)
        pulse = abs(math.sin(elapsed * 10))
        
        for bolt in self.bolts:
            bx = x + 32 + math.cos(bolt["angle"]) * bolt["distance"]
            by = y + 32 + math.sin(bolt["angle"]) * bolt["distance"]
            
            flicker = int(200 * intensity * (0.5 + 0.5 * pulse * bolt["speed"]))
            alpha = min(255, flicker)
            
            size = int(bolt["size"] * (0.8 + 0.2 * pulse))
            
            lightning_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            
            points = self._generate_lightning_bolt(size, bolt["phase"] + elapsed * 5)
            if points:
                pygame.draw.lines(
                    lightning_surface, 
                    (255, 255, 0, alpha), 
                    False, 
                    [(p[0] + size, p[1] + size) for p in points],
                    3
                )
                pygame.draw.lines(
                    lightning_surface, 
                    (255, 255, 255, alpha), 
                    False, 
                    [(p[0] + size, p[1] + size) for p in points],
                    1
                )
            
            screen.blit(lightning_surface, (int(bx - size), int(by - size)))
        
        if self.text:
            if self.text_surface is None:
                self.text_surface = self.font.render(self.text, True, (255, 255, 0), (0, 0, 0))
            
            tx = x + 32 - self.text_surface.get_width() // 2
            ty = y - 50
            screen.blit(self.text_surface, (tx, ty))
    
    def _generate_lightning_bolt(self, size: int, seed: float) -> list[tuple[int, int]]:
        points = [(size, 0)]
        segments = 4
        for i in range(1, segments + 1):
            y = int(size * i / segments)
            x_offset = int((math.sin(seed * i + i) * size * 0.4))
            points.append((size + x_offset, y))
        points.append((size, size * 2))
        return points
    
    def deactivate(self) -> None:
        self.active = False
        self.text_surface = None
