"""
Clase base Entity — representa a la mascota en pantalla.
"""

import pygame
from config import ANIMATION_DELAYS, SPRITE_SIZE


class Entity:
    def __init__(self, x: float, y: float, animations: dict) -> None:
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

        self.animations = animations
        self.state = "idle"
        self.direction = "right"

        self.frame_index = 0
        self._anim_timer = 0.0
        self.next_state = None

        self.is_sleeping = False
        self.on_ground = True
        self.ground_y = y

        self.dragging = False
        self.drag_offset_x = 0.0
        self.drag_offset_y = 0.0

        self.falling_after_drag = False
        self.dust_active = False

        self._state_timer = 0.0
        self._state_duration = 0.0

    # ── Estado ────────────────────────────────────────────────────────

    def set_state(self, new_state: str, duration: float = 0.0) -> None:
        """Cambia de estado y resetea animación y temporizadores."""
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0
            self._anim_timer = 0.0
            self._state_duration = duration
            self._state_timer = 0.0

    def should_return_to_idle(self, dt: float) -> bool:
        """
        Acumula dt real y devuelve True cuando el estado temporal expira.
        Corrige el bug anterior que asumía 60 FPS fijos.
        """
        if self._state_duration > 0:
            self._state_timer += dt
            if self._state_timer >= self._state_duration:
                return True
        return False

    # ── Hit-testing ───────────────────────────────────────────────────

    def contains_point(self, px: int, py: int) -> bool:
        rect = pygame.Rect(int(self.x), int(self.y), SPRITE_SIZE, SPRITE_SIZE)
        return rect.collidepoint(px, py)

    # ── Drag ──────────────────────────────────────────────────────────

    def start_drag(self, mouse_x: int, mouse_y: int) -> None:
        self.dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y
        self.vx = 0.0
        self.vy = 0.0

    def end_drag(self) -> None:
        self.dragging = False
        if self.y < self.ground_y - 10:
            self.on_ground = False
            self.falling_after_drag = True
            self.vy = 0.0

    # ── Física ────────────────────────────────────────────────────────

    def apply_physics(self, dt: float, gravity: float = 1200.0) -> None:
        """Aplica gravedad solo cuando está en el aire tras un drag."""
        if self.falling_after_drag and not self.on_ground:
            self.vy += gravity * dt
            self.y += self.vy * dt

            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.vy = 0.0
                self.on_ground = True
                self.falling_after_drag = False
                self.dust_active = True

    # ── Animación ─────────────────────────────────────────────────────

    def _resolve_anim_key(self) -> str:
        """Resuelve la clave de animación correcta con fallback."""
        key = f"{self.state}_{self.direction}"
        if key in self.animations:
            return key
        fallback = [k for k in self.animations if self.state in k]
        return fallback[0] if fallback else next(iter(self.animations))

    def update_animation(self, dt: float = 0.0) -> None:
        """
        Avanza el frame de animación usando dt real.

        Nota: dt es opcional para compatibilidad con llamadas sin argumento,
        pero se recomienda pasarlo siempre desde el bucle principal.
        """
        # Procesar cambio de estado pendiente
        if self.next_state:
            self.set_state(self.next_state)
            self.next_state = None
            return

        delay = ANIMATION_DELAYS.get(self.state, 0.2)
        self._anim_timer += dt if dt > 0 else (1 / 60)

        if self._anim_timer >= delay:
            self._anim_timer = 0.0
            key = self._resolve_anim_key()
            frames = self.animations[key]
            self.frame_index = (self.frame_index + 1) % len(frames)

            # Al terminar yawn, pasar a sleep
            if self.state == "yawn" and self.frame_index == 0:
                self.next_state = "sleep"

    def get_current_frame(self) -> pygame.Surface:
        key = self._resolve_anim_key()
        frames = self.animations[key]
        return frames[min(self.frame_index, len(frames) - 1)]

    # ── Render ────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """
        Dibuja el frame actual en pantalla.

        Las animaciones _left ya están pre-flipped en el diccionario de
        animaciones — NO se aplica ningún flip adicional aquí.
        """
        frame = self.get_current_frame()
        screen.blit(frame, (int(self.x), int(self.y)))
