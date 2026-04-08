"""
Entity class representing the animated character.
"""

import time
import pygame

from config import ANIMATION_DELAYS


class Entity:
    def __init__(self, x: float, y: float, animations: dict):
        self.x = x
        self.y = y
        self.animations = animations
        self.state = "idle"
        self.direction = "right"
        self.frame_index = 0
        self.last_update = time.time()
        self._state_timer: float | None = None
        self._last_state_change = time.time()
    
    def set_state(self, new_state: str, duration: float | None = None) -> None:
        """Change animation state, resetting frame index."""
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0
            self._last_state_change = time.time()
            self._state_timer = duration
    
    def should_return_to_idle(self) -> bool:
        """Check if timed state should transition back to idle."""
        if self._state_timer is not None:
            elapsed = time.time() - self._last_state_change
            if elapsed >= self._state_timer:
                return True
        return False
    
    def update_animation(self) -> None:
        """Update animation frame based on current state and timing."""
        now = time.time()
        delay = ANIMATION_DELAYS.get(self.state, 0.2)
        
        if now - self.last_update > delay:
            self.last_update = now
            key = f"{self.state}_{self.direction}"
            
            if key not in self.animations:
                key = list(self.animations.keys())[0]
            
            frames = self.animations[key]
            self.frame_index = (self.frame_index + 1) % len(frames)
    
    def get_current_frame(self) -> pygame.Surface:
        """Get the current animation frame."""
        key = f"{self.state}_{self.direction}"
        
        if key not in self.animations:
            fallback_keys = [k for k in self.animations.keys() if self.state in k]
            key = fallback_keys[0] if fallback_keys else list(self.animations.keys())[0]
        
        frames = self.animations[key]
        return frames[min(self.frame_index, len(frames) - 1)]
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the entity on the screen."""
        frame = self.get_current_frame()
        screen.blit(frame, (int(self.x), int(self.y)))
    
    @property
    def rect(self) -> pygame.Rect:
        """Get collision rect for click detection."""
        return pygame.Rect(int(self.x), int(self.y), 64, 64)
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is within entity bounds."""
        return self.rect.collidepoint(x, y)
