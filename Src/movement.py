import math
from config import SPEED, STOP_DISTANCE

def move_towards(entity, target_x, target_y):
    dx = target_x - entity.x
    dy = target_y - entity.y

    distance = math.sqrt(dx**2 + dy**2)

    if distance > STOP_DISTANCE:
        entity.set_state("walk")

        if dx > 0:
            entity.direction = "right"
        else:
            entity.direction = "left"

        entity.x += (dx / distance) * SPEED
        entity.y += (dy / distance) * SPEED
    else:
        entity.set_state("idle")