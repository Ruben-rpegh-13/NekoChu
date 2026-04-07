import time

class Entity:
    def __init__(self, x, y, animations):
        self.x = x
        self.y = y

        self.animations = animations
        self.state = "idle"
        self.direction = "right"

        self.frame_index = 0
        self.last_update = time.time()
        self.frame_delay = 0.15

    def update_animation(self):
        now = time.time()
        if now - self.last_update > self.frame_delay:
            self.frame_index += 1
            self.last_update = now

    def get_current_frame(self):
        key = f"{self.state}_{self.direction}"
        frames = self.animations[key]
        return frames[self.frame_index % len(frames)]

    def draw(self, screen):
        frame = self.get_current_frame()
        screen.blit(frame, (int(self.x), int(self.y)))