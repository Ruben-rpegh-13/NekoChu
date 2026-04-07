import time
from config import ANIMATION_DELAYS

class Entity:
    def __init__(self, x, y, animations):
        self.x = x
        self.y = y

        self.animations = animations
        self.state = "idle"
        self.direction = "right"

        self.frame_index = 0
        self.last_update = time.time()

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0

    def update_animation(self):
        delay = ANIMATION_DELAYS[self.state]
        now = time.time()

        if now - self.last_update > delay:
            self.frame_index += 1
            self.last_update = now

    def get_current_frame(self):
        key = f"{self.state}_{self.direction}"
        frames = self.animations[key]
        return frames[self.frame_index % len(frames)]

    def draw(self, screen):
        frame = self.get_current_frame()
        screen.blit(frame, (int(self.x), int(self.y)))