import math
from config import SPEED, WALK_THRESHOLD, GRAVITY, JUMP_STRENGTH


def move_towards(entity, target_x, target_y, dt=1 / 60):
    """Move entity towards target with acceleration-based movement."""
    dx = target_x - (entity.x + 32)
    dy = target_y - entity.y

    distance = math.sqrt(dx**2 + dy**2)

    if distance > WALK_THRESHOLD:
        entity.set_state("walk")
        entity.direction = "right" if dx > 0 else "left"

        dx_norm = dx / distance if distance > 0 else 0
        dy_norm = dy / distance if distance > 0 else 0

        entity.vx = dx_norm * SPEED
        entity.vy = dy_norm * SPEED
    else:
        entity.set_state("idle")
        entity.vx = 0
        entity.vy = 0

    entity.update_position(target_x, target_y)


def apply_gravity(entity, dt):
    """Apply gravity and update vertical position."""
    if not entity.on_ground and not entity.dragging:
        entity.vy += GRAVITY * dt
        entity.y += entity.vy * dt

        if entity.y >= entity.ground_y:
            entity.y = entity.ground_y
            entity.vy = 0
            entity.on_ground = True
            entity.dust_active = True


def jump(entity):
    """Make entity jump if on ground."""
    if entity.on_ground and not entity.dragging:
        entity.vy = JUMP_STRENGTH
        entity.on_ground = False
