import time
import pygame
from config import ANIMATION_DELAYS, SPRITE_SIZE, ANNOYANCE_DURATION, RAGE_DURATION


class Entity:
    def __init__(self, x, y, animations):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

        self.animations = animations
        self.state = "idle"
        self.direction = "right"

        self.frame_index = 0
        self.last_update = time.time()
        self.next_state = None

        self.last_mouse_move = time.time()
        self.yawn_delay = 3
        self.sleep_delay = 6
        self.is_sleeping = False

        self.on_ground = True
        self.ground_y = y

        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.falling_after_drag = False
        self.dust_active = False

        self._state_timer = 0
        self._state_duration = 0

    def set_state(self, new_state, duration=0):
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0
            self.last_update = time.time()
            self._state_duration = duration
            self._state_timer = 0

    def contains_point(self, px, py):
        rect = pygame.Rect(int(self.x), int(self.y), SPRITE_SIZE, SPRITE_SIZE)
        return rect.collidepoint(px, py)

    def should_return_to_idle(self):
        if self._state_duration > 0:
            self._state_timer += 1 / 60
            if self._state_timer >= self._state_duration:
                return True
        return False

    def start_drag(self, mouse_x, mouse_y):
        self.dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y
        self.vx = 0
        self.vy = 0

    def end_drag(self):
        self.dragging = False
        if self.y < self.ground_y - 10:
            self.on_ground = False
            self.falling_after_drag = True
            self.vy = 0

    def apply_physics(self, dt, gravity=1200):
        if self.falling_after_drag and not self.on_ground:
            self.vy += gravity * dt
            self.y += self.vy * dt

            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.vy = 0
                self.on_ground = True
                self.falling_after_drag = False
                self.dust_active = True

    def update_position(self, mx, my):
        if self.dragging:
            self.x = mx - self.drag_offset_x
            self.y = my - self.drag_offset_y
        else:
            self.x += self.vx
            self.y += self.vy

            if self.on_ground:
                self.y = self.ground_y

    def update_animation(self):
        now = time.time()

        if self.next_state and now >= self.last_update:
            self.set_state(self.next_state)
            self.next_state = None
            return

        delay = ANIMATION_DELAYS.get(self.state, 0.2)

        if now - self.last_update > delay:
            self.last_update = now
            key = f"{self.state}_{self.direction}"

            if key not in self.animations:
                fallback_keys = [k for k in self.animations.keys() if self.state in k]
                if fallback_keys:
                    key = fallback_keys[0]
                else:
                    key = list(self.animations.keys())[0]

            frames = self.animations[key]
            self.frame_index = (self.frame_index + 1) % len(frames)

            if self.state == "yawn" and self.frame_index == 0:
                self.next_state = "sleep"
                self.last_update = now + 0.3

    def get_current_frame(self):
        key = f"{self.state}_{self.direction}"

        if key not in self.animations:
            fallback_keys = [k for k in self.animations.keys() if self.state in k]
            key = fallback_keys[0] if fallback_keys else list(self.animations.keys())[0]

        frames = self.animations[key]
        return frames[min(self.frame_index, len(frames) - 1)]

    def draw(self, screen):
        frame = self.get_current_frame()
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (int(self.x), int(self.y)))
