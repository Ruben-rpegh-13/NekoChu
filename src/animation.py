import pygame
from PIL import Image


def load_gif_frames(path):
    """Load animated GIF and return list of pygame surfaces."""
    frames = []
    try:
        gif = Image.open(path)
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.copy().convert("RGBA")
            pygame_frame = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            )
            frames.append(pygame_frame)
    except Exception as e:
        print(f"Error loading GIF {path}: {e}")
    return frames


def load_sprite_sheet(path, frame_width, frame_height):
    """Load and parse a sprite sheet into a 2D array of frames."""
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    sheet_width, sheet_height = sheet.get_size()

    for y in range(0, sheet_height, frame_height):
        row = []
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface((x, y, frame_width, frame_height))
            row.append(frame)
        frames.append(row)

    return frames


class Animation:
    """Simple animation handler for sprite sequences."""

    def __init__(self, frames, speed=0.1):
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def reset(self):
        self.current_frame = 0
        self.timer = 0

    def get_frame(self):
        return self.frames[self.current_frame]

    @property
    def is_loop_complete(self):
        return self.current_frame == 0 and self.timer < self.speed
