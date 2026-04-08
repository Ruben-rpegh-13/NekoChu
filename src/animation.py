"""
Sprite sheet loading and animation utilities.
"""

import pygame


def load_sprite_sheet(path: str, frame_width: int, frame_height: int) -> list[list[pygame.Surface]]:
    """
    Load a sprite sheet and extract individual frames.
    
    Args:
        path: Path to the sprite sheet image
        frame_width: Width of each frame in pixels
        frame_height: Height of each frame in pixels
    
    Returns:
        2D list of pygame.Surface objects (row-major order)
    """
    sheet = pygame.image.load(path).convert_alpha()
    frames: list[list[pygame.Surface]] = []
    
    sheet_width, sheet_height = sheet.get_size()
    
    for y in range(0, sheet_height, frame_height):
        row: list[pygame.Surface] = []
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface((x, y, frame_width, frame_height))
            row.append(frame)
        frames.append(row)
    
    return frames
