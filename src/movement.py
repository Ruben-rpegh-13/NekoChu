"""
Movement logic for entities.
"""

import math

from config import SPEED, STOP_DISTANCE


def move_towards(entity, target_x: float, target_y: float) -> None:
    """
    Move entity towards target coordinates.
    
    Args:
        entity: Entity with x, y attributes
        target_x: Target X coordinate
        target_y: Target Y coordinate
    """
    dx = target_x - entity.x
    dy = target_y - entity.y
    
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance > STOP_DISTANCE:
        entity.set_state("walk")
        entity.direction = "right" if dx > 0 else "left"
        entity.x += (dx / distance) * SPEED
        entity.y += (dy / distance) * SPEED
    else:
        entity.set_state("idle")
