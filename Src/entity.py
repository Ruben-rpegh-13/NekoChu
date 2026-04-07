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
        self.next_state = None

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0

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
                key = (
                    f"{self.state}_right"
                    if "right" in list(self.animations.keys())[0]
                    else list(self.animations.keys())[0]
                )

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
        screen.blit(frame, (int(self.x), int(self.y)))
